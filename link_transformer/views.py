import hashlib
import uuid
from django.views.generic import TemplateView, View, RedirectView
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.defaults import bad_request, page_not_found
from django.shortcuts import render
from .forms import FullURLInputForm, URLHash
from .models import URL, User, UserLink
from .handlers import collect_user_data


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
        user_data = collect_user_data(request.META)
        user_data_hash = hashlib.sha224(user_data.encode()).hexdigest()

        # check user exists. If user doesn't - create one
        user = User.objects.filter(user_hash=user_data_hash).first()
        if not user:
            user = User(user_hash=user_data_hash)
            user.save()

        # collect links user created already
        user_link = UserLink.objects.filter(
            url_id__origin_url=form.cleaned_data['input_url'], user_id__user_hash=user.user_hash
        ).first()

        if user_link:
            return HttpResponse("yes")

        # generate short URL
        url_hash = hashlib.shake_256(str(uuid.uuid4()).encode()).hexdigest(5)
        short_url = f"{request.build_absolute_uri('/')}{url_hash}"

        # get url instance. If URL doesn't exist create one
        url = URL.objects.filter(origin_url=form.cleaned_data['input_url']).first()
        if not url:
            url = URL(origin_url=form.cleaned_data['input_url'])
            url.save()

        # create user link
        user_link = UserLink(url_id=url, user_id=user, short_url=short_url)
        user_link.save()

        return render(request, 'link_transformer/short-url.html', {"short_url": short_url})


class ShortURLDispatcher(RedirectView):
    def get(self, request, *args, **kwargs):
        form = URLHash(kwargs)

        # check if given data is valid
        if not form.is_valid():
            return page_not_found(request, None)

        # check if given url is present
        db_data = URL.objects.filter(url_hash=form.cleaned_data['url_hash']).first()
        if not db_data:
            return page_not_found(request, None)

        # collect user data
        user_data = collect_user_data(request.META)
        user_data_hash = hashlib.sha224(user_data.encode()).hexdigest()


        return HttpResponseRedirect(db_data.origin_url)
