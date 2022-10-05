from django import forms


class FullURLInputForm(forms.Form):
    """
    Full URL input form validator
    """
    input_url = forms.URLField(label='input_url', max_length=500)
