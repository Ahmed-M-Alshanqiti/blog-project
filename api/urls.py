from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import get_notes
from django.urls import path, include
from Chat.views import (
    ConversationListView,
    ConversationCreateView,
    MessageListView,
    MessageCreateView,
)

chat_urls = [
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
    path("conversations/create/", ConversationCreateView.as_view(), name="conversation-create"),
    path("conversations/<int:conversation_id>/messages/", MessageListView.as_view(), name="message-list"),
    path("conversations/<int:conversation_id>/messages/create/", MessageCreateView.as_view(), name="message-create"),
]

urlpatterns = [
    path('', include('blog.urls')),
    path('posts/', include('posts.urls')),
    path('user/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', get_notes, name='get_notes'),
    path("chat/", include((chat_urls, "chat"))),
]


