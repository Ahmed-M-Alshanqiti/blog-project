from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  (
    FollowView,
    get_user_profile,
    FollowerShow

)

from .auth.auth import (
    RegisterView,
    LogoutView,
    RestPassowrdInitiate,
    PasswordResetConfirmView,
    ChangePasswordView,
    Chanage_UserName,
    Chanage_Email,
    
) 

router = DefaultRouter()

urlpatterns = [
    
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),  
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("follow/<int:id>", FollowView.as_view(), name="follow"),
    path('getuser/<int:id>', get_user_profile, name='get_user_profile'),
    path('getusername/<str:username>', get_user_profile, name='get_user_profile_by_username'),
    path("", include(router.urls)),
    path(
        'password-reset/initiate/', 
        RestPassowrdInitiate.as_view(), 
        name='password_reset_initiate'
    ),
    path(
        'password-reset/confirm/', 
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),

 
    path(
        'password/change/', 
        ChangePasswordView.as_view(), 
        name='change_password_authenticated'
    ),
    

    path(
        'profile/change-username/', 
        Chanage_UserName.as_view(), 
        name='change_username'
    ),
    

    path(
        'profile/change-email/', 
        Chanage_Email.as_view(), 
        name='change_email'
    ),

    path(
        'FollowerShow',
        FollowerShow.as_view(),
        name="ShowTheFollowers"

    )
]
