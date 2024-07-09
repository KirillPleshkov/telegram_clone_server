import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from authentication.websocket.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_clone_server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(
        ws_urlpatterns
    ))
})
