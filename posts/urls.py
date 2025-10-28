from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import PostViewSet, CommentViewSet, create_post

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('create-post/',create_post,name='create_post')
]
