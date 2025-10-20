from django.db import models
from django.conf import settings

# Create your models here.

class Note(models.Model):
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



