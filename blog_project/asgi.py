import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()

from .jwt_auth_middleware import JWTAuthMiddlewareStack
import Chat.routing
import notifications.routing
import posts.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Chat.routing.websocket_urlpatterns +
            notifications.routing.websocket_urlpatterns +
            posts.routing.websocket_urlpatterns+
            notifications.routing.websocket_urlpatterns
        )
    ),
})