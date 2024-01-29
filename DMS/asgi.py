import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import I2Connect.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DMS.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            I2Connect.routing.websocket_urlpatterns
        )
    ),
})
