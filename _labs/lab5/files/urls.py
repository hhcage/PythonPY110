from django.urls import path
from .views import login_view

app_name = 'app_login'

urlpatterns = [
    path('', login_view, name="login_view"),
]