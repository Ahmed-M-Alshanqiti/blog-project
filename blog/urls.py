from django.urls import path 
from . import views

urlpatterns = [
    path('', views.firstPage, name='first-page'),
]