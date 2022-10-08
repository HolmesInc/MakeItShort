import hashlib
import uuid
from django.views.generic import TemplateView, View, RedirectView
from django.http.response import HttpResponseRedirect
from django.views.defaults import bad_request, page_not_found
from django.shortcuts import render
from .forms import FullURLInputForm, URLHash
from .models import URL, User, UserLink, LinkClick
from .handlers import create_user_hash


class FullURLInput(TemplateView):
    """
    Index page view
    """
    template_name = 'link_transformer/index.html'


class ShortURLOutput(View):
    """
    URL processing results view
    """
    template_name = 'link_transformer/short-url.html'

    def post(self, request, *args, **kwargs):
        """
        Process entered URL to make it short
        :param request: incoming request with entered full url
        :return: short url if request data if valid, Bad Request exception otherwise
        """
        form = FullURLInputForm(request.POST)

        # check that request data is valid
        if not form.is_valid():
            return bad_request(request, None)

        # since there is no access control - collect user data to identify they
        user_data_hash = create_user_hash(request.META)

        # check user exists. If user doesn't - create one
        user = User.objects.filter(user_hash=user_data_hash).first()
        if not user:
            user = User(user_hash=user_data_hash)
            user.save()

        # collect links user created already
        user_link = UserLink.objects.filter(
            url_id__origin_url=form.cleaned_data['input_url'], user_id__user_hash=user.user_hash
        ).first()

        # create short link
        if not user_link:
            # generate short URL
            url_hash = hashlib.shake_256(str(uuid.uuid4()).encode()).hexdigest(5)
            short_url = f"{request.build_absolute_uri('/')}{url_hash}"

            # get url instance. If URL doesn't exist create one
            url = URL.objects.filter(origin_url=form.cleaned_data['input_url']).first()
            if not url:
                url = URL(origin_url=form.cleaned_data['input_url'])
                url.save()

            # create user link
            user_link = UserLink(url_id=url, user_id=user, short_url=short_url, url_hash=url_hash)
            user_link.save()

        # collect amount of clicks on a short link
        clicks = LinkClick.objects.filter(user_link=user_link).count()
        return render(
            request, 'link_transformer/short-url.html', {"short_url": user_link.short_url, "link_clicks": clicks}
        )


class ShortURLDispatcher(RedirectView):
    """
    Short link redirect view
    """
    def get(self, request, *args, **kwargs):
        """
        Process redirect to origin URL from short URL
        :param request: incoming request with entered full url
        :return: origin page based on short link, page not found if short link is not known
        """
        form = URLHash(kwargs)

        # check if given data is valid
        if not form.is_valid():
            return page_not_found(request, None)

        # generate user hash
        user_data_hash = create_user_hash(request.META)

        # check if given url is present
        user_link = UserLink.objects.filter(
            url_hash=form.cleaned_data['url_hash'], user_id__user_hash=user_data_hash
        ).first()
        if not user_link:
            return page_not_found(request, None)

        # save click on user short link
        LinkClick(user_link=user_link).save()

        return HttpResponseRedirect(user_link.url_id.origin_url)
