# urls.py in app_store

from django.urls import path
from .views import weather_view

urlpatterns = [
    path('', weather_view),
]
