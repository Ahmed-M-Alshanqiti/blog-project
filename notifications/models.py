# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('message', 'Message'),
    )

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES,default="")
    message = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.type} → {self.recipient}"