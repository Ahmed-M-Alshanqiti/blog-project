# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='chat_inbox'),
    path('<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('search/', views.search_users, name='chat_search'),
    path('create/<int:user_id>/', views.create_conversation, name='create_conversation'),
]