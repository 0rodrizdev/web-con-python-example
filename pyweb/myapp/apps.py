import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import ChatMessage  # Asegúrate de que este modelo esté definido en tu models.py

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Se obtiene el nombre del grupo (sala de chat) desde la URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Únete al grupo de sala de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Acepta la conexión
        await self.accept()

    async def disconnect(self, close_code):
        # Sale del grupo de sala de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Método para recibir un mensaje del WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']  # Suponiendo que también se envía el usuario

        # Guarda el mensaje en la base de datos
        await self.save_message(user, message)

        # Envía el mensaje a todos los miembros del grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )

    # Método para recibir mensajes del grupo
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Enviar el mensaje a través del WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        # Guarda el mensaje en la base de datos
        chat_message = ChatMessage(user=user, message=message)  # Cambia según tu modelo
        chat_message.save()

    @database_sync_to_async
    def get_messages(self):
        # Obtén los mensajes de la base de datos
        return list(ChatMessage.objects.all().values('user', 'message'))

# Si deseas implementar más consumidores, puedes hacerlo de la siguiente manera:
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'notifications_{self.user.id}'

        # Únete al grupo de notificaciones
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def notify(self, event):
        notification = event['notification']
        
        await self.send(text_data=json.dumps({
            'notification': notification,
        }))

    async def receive(self, text_data):
        # Puedes manejar la recepción de mensajes aquí si es necesario
        pass
