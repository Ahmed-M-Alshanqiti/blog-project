from django.shortcuts import render
from posts import models as post_models
from users import models as user_models

# Create your views here.

def firstPage(requist):
    
    posts = post_models.Post.objects.all().order_by('-created_at')
    users = user_models.User.objects.all()

    return render(requist , 'first.html',{'posts':posts, 'users':users})