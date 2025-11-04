from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_unread_count(user):
    from .models import Notification
    return Notification.objects.filter(recipient=user, is_read=False).count()

@database_sync_to_async
def mark_as_read(notif_id, user):
    from .models import Notification
    Notification.objects.filter(id=notif_id, recipient=user).update(is_read=True)

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser) or not self.user.is_authenticated:
            await self.close(code=4003) 
            return

        self.group_name = f"notifications_user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept() 

        count = await get_unread_count(self.user)
        await self.send_json({
            "type": "unread_count",
            "count": count
        })

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        if content.get("type") == "mark_read":
            notif_id = content["id"]
            await mark_as_read(notif_id, self.user)
            count = await get_unread_count(self.user)
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "unread_count_update", "count": count}
            )

    async def notification_created(self, event):
        await self.send_json({
            "type": "new_notification",
            "notification": event["notification"]
        })

    async def unread_count_update(self, event):
        await self.send_json({
            "type": "unread_count",
            "count": event["count"]
        })