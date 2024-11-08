from django.urls import re_path
from . import ws_consumer 

websocket_urlpatterns = [
    re_path(r"^ws/$", ws_consumer.CamWSConsumer.as_asgi()),
]