
from django.urls import path
from .views import get_celebrity_bio, autocomplete_celebrity

urlpatterns = [
    path('', get_celebrity_bio, name='get_celebrity_bio'),
    path('autocomplete/', autocomplete_celebrity, name='autocomplete_celebrity'),
]
