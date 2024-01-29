# DMS/urls.py

from django.urls import include, path

urlpatterns = [
    # other paths...
    path('I2Connect/', include('I2Connect.urls')),
]
