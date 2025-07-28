import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import rides.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RideSafe.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            rides.routing.websocket_urlpatterns
        )
    ),
})
