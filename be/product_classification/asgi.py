"""
ASGI config for product_classification project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import ws_camera.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_classification.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        ws_camera.routing.websocket_urlpatterns
    ),
})

