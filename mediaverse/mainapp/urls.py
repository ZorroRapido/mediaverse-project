from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('search/', search, name="search_results")
]
