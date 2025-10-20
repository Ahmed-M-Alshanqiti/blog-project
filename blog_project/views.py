from django.shortcuts import render
from posts  import models

# Create your views here.
def home(request):
    Posts = models.Post.objects.all().order_by('-created_at')
    
    return render(request, 'base.html', {'posts':Posts})

