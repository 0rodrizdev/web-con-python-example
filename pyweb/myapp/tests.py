from django.test import TestCase
from .models import ChatRoom, Message
from channels.testing import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from .consumers import ChatConsumer
import json

class ChatRoomModelTests(TestCase):
    def setUp(self):
        self.room = ChatRoom.objects.create(name="test_room")

    def test_chat_room_creation(self):
        self.assertEqual(self.room.name, "test_room")
        self.assertTrue(ChatRoom.objects.filter(name="test_room").exists())

class MessageModelTests(TestCase):
    def setUp(self):
        self.room = ChatRoom.objects.create(name="test_room")
        self.message = Message.objects.create(room=self.room, user="test_user", content="Hello, World!")

    def test_message_creation(self):
        self.assertEqual(self.message.content, "Hello, World!")
        self.assertEqual(self.message.room.name, "test_room")
        self.assertEqual(self.message.user, "test_user")

class ChatConsumerTests(ChannelsLiveServerTestCase):
    async def test_chat_consumer(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/test_room/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending a message
        await communicator.send_json_to({
            'type': 'chat_message',
            'message': 'Hello!',
            'user': 'test_user'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Hello!')
        self.assertEqual(response['user'], 'test_user')

        # Close the connection
        await communicator.disconnect()

    async def test_private_chat_consumer(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/private/test_user/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending a private message
        await communicator.send_json_to({
            'type': 'private_message',
            'message': 'Hello, private!',
            'user': 'test_user'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Hello, private!')
        self.assertEqual(response['user'], 'test_user')

        # Close the connection
        await communicator.disconnect()

