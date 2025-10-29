import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LikeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.group_name = f"post_likes_{self.post_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()                    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def like_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "like_count_update",
            "likes_count": event["likes_count"]
        }))