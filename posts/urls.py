from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import (
    # PostViewSet,
    # CommentViewSet,
    create_post,
    PostLikeToggleView,
)
# router = DefaultRouter()
# router.register(r'posts', PostViewSet, basename='post')
# router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('create-post/',create_post,name='create_post'),
    path('post/<int:post_id>/like/', PostLikeToggleView, name='post-like-toggle'),
    ]
