from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from .. import models as post_models
from notifications.views import send_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



Post = post_models.Post.objects.all()
# ------------------------------------------------------------------
# UNUSED DRF IMPORTS – keep for later
# ------------------------------------------------------------------
# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from ..serializer import PostSerializer, CommentSerializer
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

# ------------------------------------------------------------------
# DRF ViewSets – **commented out**
# ------------------------------------------------------------------
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = post_models.Post.objects.all().order_by('-created_at')
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     parser_classes = [MultiPartParser, FormParser]
#
#     @method_decorator(cache_page(60 * 2, key_prefix='post_list'))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def like(self, request, pk=None):
#         ...

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = post_models.Comment.objects.all().order_by('created_at')
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# ------------------------------------------------------------------
# HTML / template views
# ------------------------------------------------------------------
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def sharePost(request):
    return render(request, 'share.html')


def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        post = post_models.Post.objects.create(user=request.user, title=title)

        block_types = request.POST.getlist("block_type[]")
        text_contents = request.POST.getlist("text_content[]")
        all_files = list(request.FILES.values())
        file_idx = 0

        for i, btype in enumerate(block_types):
            text = text_contents[i] if i < len(text_contents) else ""
            media = None
            if btype in ("image", "video") and file_idx < len(all_files):
                media = all_files[file_idx]
                file_idx += 1

            post_models.PostContent.objects.create(
                post=post,
                order=i,
                content_type=btype,
                text_content=text if btype == "text" else "",
                media_file=media,
            )
        messages.success(request, "Post created successfully!")
        return redirect("first-page")

    return render(request, "share.html")


@login_required
@require_POST
def PostLikeToggleView(request, post_id):
    post = get_object_or_404(post_models.Post, id=post_id)
    user = request.user

    already_liked = post.likes.filter(id=user.id).exists()

    if already_liked:
        post.likes.remove(user)
        action = "unliked"
        liked = False
    else:
        post.likes.add(user)
        action = "liked"
        liked = True

        if post.user != user:
            send_notification(
                recipient=post.user,
                actor=user,
                type="like",
                message=f"@{user.username} liked your post.",
                post=post
            )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"post_likes_{post.id}",
        {
            "type": "like_update",
            "likes_count": post.likes.count()
        }
    )

    return JsonResponse({
        "status": action,
        "liked": liked,
        "likes_count": post.likes.count()
    })