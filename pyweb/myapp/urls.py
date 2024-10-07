from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

    # Ruta para la página principal
    path('', views.IndexView.as_view(), name='index'),

    # Ruta para el chat
    path('chat/<str:room_name>/', views.ChatRoomView.as_view(), name='chat_room'),

    # Ruta para el perfil del usuario
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),

    # Rutas de API (si estás utilizando Django REST framework)
    path('api/', include('myapp.api.urls')),

    # Ruta para mensajes privados
    path('private/<str:username>/', views.PrivateChatView.as_view(), name='private_chat'),

    # Otras rutas que desees agregar
    # path('about/', views.AboutView.as_view(), name='about'),
]

