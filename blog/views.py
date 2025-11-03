from django.shortcuts import render
from posts import models as post_models
from notifications import models as notifcation_model


def firstPage(request):

    posts = post_models.Post.objects.all().order_by('-created_at').prefetch_related(
        'content_blocks', 
        'likes'
    ).select_related('user')
    # notifications = notifcation_model.Notification.objects.all().order_by('-created_at').prefetch_related(
    #     'recipient',
    #     'actor',

    # ).select_related('user')
    
    context = {
        'posts': posts, 
    }
    
    return render(request, 'first.html', context)



