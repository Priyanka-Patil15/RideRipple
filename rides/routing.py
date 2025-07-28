from django.urls import re_path
from . import consumers

# WebSocket URL patterns for chat
websocket_urlpatterns = [
    re_path(r'^ws/ride/(?P<ride_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
