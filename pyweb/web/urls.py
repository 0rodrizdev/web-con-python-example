from django.urls import path
from .views import (
    IndexView,
    ChatRoomView,
    ProfileView,
    PrivateChatView,
    AboutView,
    ContactView,
    send_message,
)

urlpatterns = [
    # Ruta para la página principal
    path('', IndexView.as_view(), name='index'),

    # Ruta para la sala de chat
    path('chat/<str:room_name>/', ChatRoomView.as_view(), name='chat_room'),

    # Ruta para el perfil de un usuario
    path('user/<str:username>/', ProfileView.as_view(), name='profile'),

    # Ruta para chat privado
    path('private-chat/<str:username>/', PrivateChatView.as_view(), name='private_chat'),

    # Ruta para la página "Acerca de"
    path('about/', AboutView.as_view(), name='about'),

    # Ruta para la página de contacto
    path('contact/', ContactView.as_view(), name='contact'),

    # Ruta para enviar un mensaje en la sala de chat
    path('send_message/<str:room_name>/', send_message, name='send_message'),
]
