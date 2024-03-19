from django.urls import path
from . import views


urlpatterns = [
    path("", views.weather_ui, name='weather_ui'),
]