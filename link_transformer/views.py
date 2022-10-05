import hashlib
from django.views.generic import TemplateView, View
from django.views.defaults import bad_request
from django.shortcuts import render
from .forms import FullURLInputForm


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
        if form.is_valid():
            # generate short URL based on input URL
            url_hash = hashlib.shake_256(form.cleaned_data['input_url'].encode()).hexdigest(5)
            short_url = f"{request.build_absolute_uri('/')}{url_hash}"
            return render(request, 'link_transformer/short-url.html', {"short_url": short_url})

        else:
            return bad_request(request, None)
