# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = data.get('sender', 'Anonymous')
        message = data.get('message')

        # Save to DB
        ChatMessage.objects.create(sender=sender, message=message)

        # Broadcast to group
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "sender": sender,
                "message": message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"]
        }))
