from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..views.api_views import  (
    FollowView,
    get_user_profile,
    FollowerShow,


)
from ..views.views import(
    Login_User,
    Register_User,
    account_view,
    follow_toggle,
)

from ..auth.auth import (
    RestPassowrdInitiate,
    PasswordResetConfirmView,
    ChangePasswordView,
    Chanage_UserName,
    Chanage_Email,
    
) 

router = DefaultRouter()

urlpatterns = [
    
    path("register/", Register_User, name="register"),
    path("login/", Login_User, name="login-user"), 
    path("logout/", include("django.contrib.auth.urls")),
    path('account/', account_view, name='account'),                # own
    path('account/<str:username>/', account_view, name='profile'),
    path('follow/<int:user_id>/', follow_toggle, name='follow-toggle'),
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
