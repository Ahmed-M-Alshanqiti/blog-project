from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification


@login_required
def Notfications_update (request,Type,message,actor,target):
   
    if request.method == 'POST':
        new_notfication_create = Notification(
        recipient = target,
        actor = actor,
        Type = Type,
        message = message,
        )

        new_notfication_create.save()




    notification = Notification.objects.all().order_by('-created_at').prefetch_related(
        'actor',
        'recipient'
        'actor',
        'message',
        'is_read',
    )

    context = {
        'notfication':notification
    }
    return context




def send_notification(recipient, actor, type, message, post=None):
    notif = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        type=type,
        message=message,
        post=post
    )

    notif_data = {
        "id": notif.id,
        "actor": actor.username,
        "actor_id": actor.id,
        "type": notif.type,
        "message": notif.message,
        "post_id": post.id if post else None,
        "created_at": notif.created_at.isoformat(),
        "is_read": False
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_user_{recipient.id}",
        {
            "type": "notification_created",
            "notification": notif_data
        }
    )

    # Update unread count
    unread = Notification.objects.filter(recipient=recipient, is_read=False).count()
    async_to_sync(channel_layer.group_send)(
        f"notifications_user_{recipient.id}",
        {
            "type": "unread_count_update",
            "count": unread
        }
    )