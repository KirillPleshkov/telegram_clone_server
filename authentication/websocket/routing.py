from django.urls import path

from .consumers import QrAuthConsumer

ws_urlpatterns = [
    path('ws/qr_auth/', QrAuthConsumer.as_asgi())
]
