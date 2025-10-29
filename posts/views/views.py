from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from ..models import Post, Comment
from ..utils import send_like_notification
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializer import PostSerializer, CommentSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages
from ..models import Post, PostContent

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def sharePost(request):
    return render(request, 'share.html')

class PostViewSet(viewsets.ModelViewSet):
    print("################### the view hit ")
    queryset = Post.objects.all().order_by('-created_at')
    print("################### querry set complete ")
    serializer_class = PostSerializer
    print("################### the post serialized")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @method_decorator(cache_page(60 * 2, key_prefix='post_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("################### perform_create() called")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            return Response({"status": "unliked", "likes_count": post.likes.count()}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            post.save()
            if user != post.user:
                send_like_notification(post, user)
            return Response({"status": "liked", "likes_count": post.likes.count()}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




def create_post(request):
    print(request.POST)
    if request.method == "POST":
        print(request.FILES)
        title = request.POST.get("title", "")
        post = Post.objects.create(user=request.user, title=title)

        block_types = request.POST.getlist("block_type[]")
        text_contents = request.POST.getlist("text_content[]")
        media_files = request.FILES.getlist("media_file[]")
        uploaded_files = {
            key.split('_')[-1]: file_obj 
            for key, file_obj in request.FILES.items() 
            if key.startswith('media_file_')
        }
        all_submitted_files = list(request.FILES.values())
        media_file_index = 0
        # for i, btype in enumerate(block_types):
        #     text_content = text_contents[i] if i < len(text_contents) else ""
        #     media_file = media_files[i] if i < len(media_files) else None
        #     PostContent.objects.create(
        #         post=post,
        #         order=i,
        #         content_type=btype,
        #         text_content=text_content if btype == "text" else "",
        #         media_file=media_file if btype != "text" else None,
        #     )
        for i, btype in enumerate(block_types):
            text_content = text_contents[i] if i < len(text_contents) else ""
            current_media_file = None

            if btype in ["image", "video"]:
                # If the block is an image or video, check if there is a file
                # left in the media_files list, and use the indexer to get it.
                if media_file_index < len(all_submitted_files):
                    current_media_file = all_submitted_files[media_file_index]
                    media_file_index += 1 # Advance the index for the next file
                else:
                    # This should theoretically not happen if the HTML is right, 
                    # but it's a good safety check.
                    messages.error(request, f"Error: {btype} block requires a file.")
                    post.delete() # Cleanup the created post
                    return redirect("create_post")

            # Create the PostContent object
            PostContent.objects.create(
                post=post,
                order=i,
                content_type=btype,
                # Only save text content if it's a text block
                text_content=text_content if btype == "text" else "",
                # Only save media file if it's an image/video block
                media_file=current_media_file,
            )
        messages.success(request, "Post created successfully!")
        return redirect("first-page")

    return render(request, "share.html")

