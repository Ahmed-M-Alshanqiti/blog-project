from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import AbstractUser
import os, uuid

class User(AbstractUser):
    email = models.EmailField(unique=True)  
    
    def __str__(self):
        return self.username
    
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"  
    return os.path.join(f'profiles/user_{instance.user.id}', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    header_image = models.ImageField(upload_to="headers/", blank=True, null=True)

    def followers(self):
        return User.objects.filter(following_relations__following=self.user)

    def following(self):
        return User.objects.filter(followers_relations__follower=self.user)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relations")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_relations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")  

    def __str__(self):
        return f"{self.follower} follows {self.following}"
