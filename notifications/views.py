from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def Notfications_update (request,Type,message,actor,target):
   
    if request.method == 'POST':
        new_notfication_create = Notification(
        recipient = target,
        actor = actor,
        Type = Type,
        message = message,
        )

        new_notfication_create.save()




    notification = Notification.objects.all().order_by('-created_at').prefetch_related(
        'actor',
        'recipient'
        'actor',
        'message',
        'is_read',
    )

    context = {
        'notfication':notification
    }
    return context