from notifications.models import Notification

def send_like_notification(post, user_liking):
    """Creates a notification for the post owner."""
    
    if post.user != user_liking:
        Notification.objects.create(
            recipient=post.user,         
            actor=user_liking,       
            verb='liked',                
            target_post=post
        )