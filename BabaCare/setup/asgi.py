"""
ASGI config for setup project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from rtchat import routing

django_asgi_app = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
# Creates different types of protocols
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Authenticates the route and the instancies for the Authentication
    "websocket": AuthMiddlewareStack(
        # URLRouter routes the ws WebSocket
        URLRouter(
            routing.websocket_urlpatterns
            # websocket_urlpatterns is the list of routes for the WebSocket
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})

ASGI_APPLICATION = 'setup.asgi.application'