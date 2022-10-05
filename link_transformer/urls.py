from django.urls import path
from .views import FullURLInput, ShortURLOutput

urlpatterns = [
    path('', FullURLInput.as_view(), name='index'),
    path('make-it-short', ShortURLOutput.as_view(), name='short_url'),
]
