# I2Connect/routing.py

from django.urls import path
from .consumers import TrafficDataConsumer

websocket_urlpatterns = [
    path('ws/traffic/', TrafficDataConsumer.as_asgi()),
]
