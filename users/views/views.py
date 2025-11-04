from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from ..forms import CustomUserCreationForm 
from notifications.views import send_notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..models import  Follow

# user = User.objects.all()


def Login_User(request,user = None):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('/')  
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def Register_User(request):
    if request.user.is_authenticated:
        return redirect('first-page')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}, your account has been created!")
            return redirect('first-page')
        else:
            # Show form validation errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'Rigester.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def account_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    posts = profile_user.posts.all().order_by('-created_at')

    # PRE-CALCULATE if current user follows this profile_user
    is_following = False
    if request.user != profile_user:
        is_following = request.user.following_relations.filter(following=profile_user).exists()

    return render(request, 'account.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,  # ← Pass to template
    })
@login_required
def follow_toggle(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if request.user == target:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    # Use a transaction – safe when many users click at once
    with transaction.atomic():
        follow_obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )
        if not created:                     # already existed → unfollow
            follow_obj.delete()
            action = 'unfollowed'
        else:
            action = 'followed'

            # SEND NOTIFICATION (only when following)
            send_notification(
                recipient=target,
                actor=request.user,
                type='follow',
                message=f"@{request.user.username} started following you.",
                post=None
            )

    # Return fresh counts
    return JsonResponse({
        'action': action,
        'followers_count': target.followers_relations.count(),
        'following_count': request.user.following_relations.count(),
    })


