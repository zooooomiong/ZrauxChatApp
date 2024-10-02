import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import DuoChat, DuoMessage
from uuid import UUID
import asyncio
from .tasks import save_messages_in_db

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def save_messages(self, message):
        user_id = self.scope['user'].id
        room_name = self.room_name
        save_messages_in_db.delay(user_id, room_name, message)
        
    @sync_to_async
    def is_valid_room_for_user(self, room_name, user):
        """
        Check if the room exists and if the user is part of the chat.
        """
        try:
            chat = DuoChat.objects.get(pk=room_name)
            return user in chat.users.all()
        except DuoChat.DoesNotExist:
            return False

    async def connect(self):
        """
        Handle the WebSocket connection.
        """
        user = self.scope["user"]
        room_name = self.scope["url_route"]["kwargs"]["room_name"]

        if user.is_authenticated and await self.is_valid_room_for_user(room_name, user):
            self.room_name = room_name
            self.room_group_name = f"chat_{self.room_name}"

            # Join the room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
           
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, close_code):
        """
        Handle the WebSocket disconnection.
        """
        if hasattr(self, "room_group_name"):
            # Leave the room group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle receiving a message from WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        username = self.scope["user"].username  

        await self.save_messages(message)
        
        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": username  
                }
            )

    async def chat_message(self, event):
        """
        Handle receiving a message from the room group.
        """
        message = event["message"]
        sender = event["sender"]  # Get the sender's username from the event

        # Send message and username to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": sender  # Send the sender's username along with the message
        }))
