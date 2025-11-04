# posts/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_like_count(post_id):
    from .models import Post
    return Post.objects.filter(id=post_id).first().likes.count()

class LikeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        # Allow unauthenticated users to view (but not like)
        if user and isinstance(user, AnonymousUser):
            await self.close()
            return

        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.group_name = f"post_likes_{self.post_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send current count on connect
        count = await get_like_count(self.post_id)
        await self.send_json({
            "type": "like_count_update",
            "likes_count": count
        })

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def like_update(self, event):
        await self.send_json({
            "type": "like_count_update",
            "likes_count": event["likes_count"]
        })