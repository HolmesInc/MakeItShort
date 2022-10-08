from django import forms


class FullURLInputForm(forms.Form):
    """
    Validate full URL input form validator
    """
    input_url = forms.URLField(label='input_url', max_length=500)


class URLHash(forms.Form):
    """
    Validate URL hash
    """
    url_hash = forms.CharField(label='url_hash', min_length=9, max_length=10)
