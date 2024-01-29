# I2Connect/urls.py

from django.urls import path
from .views import traffic_view

urlpatterns = [
    path('traffic/', traffic_view, name='traffic'),
]
