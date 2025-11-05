# from rest_framework import generics, permissions
# from .models import Conversation, Message
# from .serializers import ConversationSerializer, MessageSerializer

# class ConversationListView(generics.ListAPIView):
#     serializer_class = ConversationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Conversation.objects.filter(participants=self.request.user)


# class ConversationCreateView(generics.CreateAPIView):
#     serializer_class = ConversationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         conversation = serializer.save()
#         conversation.participants.add(self.request.user)


# class MessageListView(generics.ListAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         conversation_id = self.kwargs["conversation_id"]
#         return Message.objects.filter(conversation_id=conversation_id)


# class MessageCreateView(generics.CreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         conversation_id = self.kwargs["conversation_id"]
#         conversation = Conversation.objects.get(id=conversation_id)
#         serializer.save(sender=self.request.user, conversation=conversation)




# chat/views.py
# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Conversation, Message
from users.models import User


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user).annotate(
        last_message_time=Max('messages__created_at')
    ).order_by('-last_message_time')

    for conv in conversations:
        conv.unread_count = conv.messages.filter(read=False).exclude(sender=request.user).count()
        last_msg = conv.messages.order_by('-created_at').first()
        conv.preview = last_msg.text[:50] + "..." if last_msg and last_msg.text else "No messages"

    return render(request, 'chat/inbox.html', {'conversations': conversations})


@login_required
def chat_room(request, conversation_id):
    conversation = get_object_or_404(
        Conversation, id=conversation_id, participants=request.user
    )
    messages = conversation.messages.all().order_by('created_at')
    messages.filter(read=False).exclude(sender=request.user).update(read=True)

    other_participant = conversation.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/room.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_participant
    })


@require_GET
@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'users': []})

    users = User.objects.filter(
        username__icontains=query
    ).exclude(id=request.user.id).select_related('profile').values(
        'id', 'username',
    )[:10]

    user_list = []
    for u in users:
        user_list.append({
            'id': u['id'],
            'username': u['username'],
            # 'profile_picture': u['profile__profile_picture'] or None
        })

    return JsonResponse({'users': user_list})

@login_required
def create_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=other_user).first()

    if existing:
        return redirect('chat_room', conversation_id=existing.id)

    conv = Conversation.objects.create()
    conv.participants.add(request.user, other_user)
    return redirect('chat_room', conversation_id=conv.id)