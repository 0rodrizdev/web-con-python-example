import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from myapp.routing import websocket_urlpatterns  # Asegúrate de crear este archivo
from channels.sessions import SessionMiddlewareStack

# Establece la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Obtiene la aplicación ASGI de Django
application = get_asgi_application()

# Define el enrutador de protocolos
application = ProtocolTypeRouter({
    "http": application,  # Rutas HTTP
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(  # Middleware para autenticación
            URLRouter(
                websocket_urlpatterns  # Rutas de WebSocket
            )
        )
    ),
})

