from django.db.models.signals import post_delete,post_save
from django.core.cache import cache
from .models import Post
from django.dispatch import receiver

@receiver([post_save,post_delete], sender=Post)
def invalid_the_post_cache(sender, instance,**kwargs):
    print("clearing the post cache")

    cache.delete_pattern('*post_list')
