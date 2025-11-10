import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def create_message(self, conversation_id, sender, text):
        conversation = Conversation.objects.get(id=conversation_id)
        msg = Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=text
        )
        return msg, msg.created_at

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.scope["user"]

        # ——— TYPING INDICATOR ———
        if data.get("type") == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_status",
                    "sender": sender.username,
                    "typing": data.get("typing", False)
                }
            )
            return  # ← Stop here for typing events

        # ——— REGULAR MESSAGE ———
        message = data.get("message")
        if not message:
            return

        try:
            msg, created_at = await self.create_message(
                conversation_id=self.conversation_id,
                sender=sender,
                text=message
            )
        except Conversation.DoesNotExist:
            print(f"Error: Conversation {self.conversation_id} not found.")
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": sender.username,
                "message": message,
                "created_at": str(created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"],
            "created_at": event["created_at"]
        }))

    async def typing_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "sender": event["sender"],
            "typing": event["typing"]
        }))