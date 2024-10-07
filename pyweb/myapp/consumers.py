import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom, PrivateMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumidor WebSocket para el chat.
    """

    async def connect(self):
        """
        Método llamado cuando se establece la conexión WebSocket.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Unirse al grupo de la sala de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Aceptar la conexión WebSocket

        # Cargar los mensajes antiguos al conectarse
        await self.load_previous_messages()

    async def disconnect(self, close_code):
        """
        Método llamado cuando se cierra la conexión WebSocket.
        """
        # Salir del grupo de la sala de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Método llamado al recibir un mensaje desde el WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Guardar el mensaje en la base de datos
        chat_message = await self.save_message(user, message)

        # Enviar el mensaje a la sala de chat
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat_message.message,
                'username': user.username,
                'timestamp': str(chat_message.timestamp)
            }
        )

    async def chat_message(self, event):
        """
        Método para enviar el mensaje al WebSocket.
        """
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    async def load_previous_messages(self):
        """
        Cargar mensajes anteriores en la sala de chat.
        """
        messages = await ChatMessage.objects.filter(room__name=self.room_name).order_by('timestamp').all()
        message_list = []

        for message in messages:
            message_list.append({
                'message': message.message,
                'username': message.user.username,
                'timestamp': str(message.timestamp)
            })

        await self.send(text_data=json.dumps({
            'previous_messages': message_list
        }))

    async def save_message(self, user, message):
        """
        Guardar un mensaje en la base de datos.
        """
        room = await ChatRoom.objects.get(name=self.room_name)
        chat_message = ChatMessage(user=user, room=room, message=message)
        await database_sync_to_async(chat_message.save)()
        return chat_message


class PrivateChatConsumer(AsyncWebsocketConsumer):
    """
    Consumidor WebSocket para mensajes privados.
    """

    async def connect(self):
        """
        Método llamado cuando se establece la conexión WebSocket.
        """
        self.recipient_username = self.scope['url_route']['kwargs']['username']
        self.recipient = await database_sync_to_async(User.objects.get)(username=self.recipient_username)
        self.channel_name = f'private_{self.recipient.username}'

        # Unirse al grupo de mensajes privados
        await self.channel_layer.group_add(
            self.channel_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Método llamado cuando se cierra la conexión WebSocket.
        """
        await self.channel_layer.group_discard(
            self.channel_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Método llamado al recibir un mensaje desde el WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']

        # Guardar el mensaje privado en la base de datos
        private_message = await self.save_private_message(sender, self.recipient, message)

        # Enviar el mensaje al receptor
        await self.channel_layer.group_send(
            self.channel_name,
            {
                'type': 'private_message',
                'message': private_message.message,
                'sender': sender.username,
                'timestamp': str(private_message.timestamp)
            }
        )

    async def private_message(self, event):
        """
        Método para enviar el mensaje privado al WebSocket.
        """
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    async def save_private_message(self, sender, recipient, message):
        """
        Guardar un mensaje privado en la base de datos.
        """
        private_message = PrivateMessage(sender=sender, recipient=recipient, message=message)
        await database_sync_to_async(private_message.save)()
        return private_message
