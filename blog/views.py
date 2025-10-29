from django.shortcuts import render
from posts import models as post_models



def firstPage(request):

    posts = post_models.Post.objects.all().order_by('-created_at').prefetch_related(
        'content_blocks', 
        'likes'
    ).select_related('user')
    
    context = {
        'posts': posts, 
    }
    
    return render(request, 'first.html', context)



