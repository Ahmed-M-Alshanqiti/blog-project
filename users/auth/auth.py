from rest_framework.permissions import AllowAny,IsAuthenticated
from ..models import User
# from ..serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404





from ..serializers import (
    EmailSerializer, 
    SetNewPasswordSerializer, 
    ChangePasswordSerializer, 
    ChangeUsernameSerializer, 
    ChangeEmailSerializer,
    RegisterSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)


def send_reset_email(user, uidb64, token):
    """Placeholder function to simulate sending a password reset email."""
    reset_link = f"http://yourdomain.com/reset-confirm/{uidb64}/{token}"
    print(f"--- Sending Password Reset Email to {user.email} ---")
    print(f"Reset Link: {reset_link}")
    print("-------------------------------------------------------")




class RestPassowrdInitiate(generics.GenericAPIView):
    """
    Initiates the password reset process by sending a reset link to the user's email.
    (This is the user's provided RestPassowrd view, renamed for clarity).
    Permission: AllowAny (for when the user is logged out and forgot password).
    """
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        

        user = User.objects.filter(email=email).first()
        
        if user:
            
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            

            token = PasswordResetTokenGenerator().make_token(user)
            

            send_reset_email(user, encoded_pk, token)
            

        return Response(
            {"detail": "If a matching account was found, a password reset link has been sent to your email."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Confirms the password reset token and allows the user to set a new password.
    Permission: AllowAny.
    """
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uidb64 = serializer.validated_data.get('uidb64')
        token = serializer.validated_data.get('token')
        new_password = serializer.validated_data.get('password')
        
        try:

            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, DjangoUnicodeDecodeError):
            return Response(
                {"detail": "Invalid reset link or token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {"detail": "Token is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )


        user.set_password(new_password)
        user.save()
        
        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK
        )



class ChangePasswordView(generics.GenericAPIView):
    """
    Allows an authenticated user to change their password by providing the old one.
    Permission: IsAuthenticated (for when the user is logged in).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
     
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

     
        user.set_password(new_password)
        user.save()

  
        
        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK
        )



class Chanage_UserName(generics.GenericAPIView):
    """
    Allows an authenticated user to change their username.
    Permission: IsAuthenticated.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUsernameSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_username = serializer.validated_data['new_username']
        user = request.user
        
 
        user.username = new_username
        user.save()
        
        return Response(
            {"detail": "Username updated successfully.", "new_username": new_username},
            status=status.HTTP_200_OK
        )


class Chanage_Email(generics.GenericAPIView):
    """
    Allows an authenticated user to change their email address.
    Permission: IsAuthenticated.
    """



    
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data['new_email']
        user = request.user
        

        user.email = new_email
        user.save()
        
        return Response(
            {"detail": "Email address updated successfully.", "new_email": new_email},
            status=status.HTTP_200_OK
        )
