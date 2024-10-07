from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Ruta para el chat grupal
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),

    # Ruta para los mensajes privados
    re_path(r'ws/private/(?P<username>[^/]+)/$', consumers.PrivateChatConsumer.as_asgi()),
]

