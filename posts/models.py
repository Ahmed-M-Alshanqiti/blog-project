from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid


User = settings.AUTH_USER_MODEL

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post {self.pk}: {self.title or 'Untitled'}"

    def save(self, *args, **kwargs):
        if not self.slug:

            base_slug = slugify(self.title) if self.title else str(uuid.uuid4())[:8]
            self.slug = base_slug

        super().save(*args, **kwargs)

class PostContent(models.Model):

    post = models.ForeignKey(
        Post, 
        related_name='content_blocks', 
        on_delete=models.CASCADE
    )
    
    order = models.PositiveIntegerField(db_index=True)
    
    CONTENT_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_CHOICES,
        default='text',
    )
    
    text_content = models.TextField(blank=True, null=True)
    
    media_file = models.FileField(
        upload_to='post_content_media/', 
        blank=True, 
        null=True
    )

    class Meta:
       
        ordering = ['order']

        unique_together = ('post', 'order') 

    def __str__(self):
        return f"Block {self.order} for Post {self.post.pk}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.id}: {self.content[:30]}"