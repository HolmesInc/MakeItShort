from django.urls import path
from .views import FullURLInput, ShortURLOutput, ShortURLDispatcher

app_name = 'link_transformer'
urlpatterns = [
    path('', FullURLInput.as_view(), name='index'),
    path('make-it-short', ShortURLOutput.as_view(), name='short_url'),
    path('<str:url_hash>', ShortURLDispatcher.as_view(), name='short_url_dispatcher'),
]
