from django.urls import path ,include
from . import views

urlpatterns = [
    path('home/', views.firstPage, name='first-page'),
    path('users/',include('users.urls'))
]