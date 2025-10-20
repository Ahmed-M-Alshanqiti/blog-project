from rest_framework import serializers
from .models import User, Profile, Follow
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "profile_image", "header_image"]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Profile.objects.create(user=user) 
        return user

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["follower", "following", "created_at"]

class EmailSerializer(serializers.Serializer):
    """Serializer used to accept and validate the email for password reset initiation."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email address does not exist.")
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    """Serializer used to confirm the reset token and set the new password."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    class Meta:
        fields = ('password', 'password_confirm', 'uidb64', 'token')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "New passwords must match."})
        return data

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for authenticated users to change their password."""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ('old_password', 'new_password', 'confirm_new_password')

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "New passwords must match."})

        user = self.context.get('request').user
        if not user.check_password(data['old_password']):
            raise AuthenticationFailed("Old password is not correct.", code='authentication')

        return data


class ChangeUsernameSerializer(serializers.Serializer):
    """Serializer for authenticated users to change their username."""
    new_username = serializers.CharField(required=True, max_length=150)

    def validate_new_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

class ChangeEmailSerializer(serializers.Serializer):
    """Serializer for authenticated users to change their email."""
    new_email = serializers.EmailField(required=True)

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

class FollowerSerializer(serializers.ModelSerializer):

    follower_details = UserSerializer(source='follower', read_only=True) 

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_details', 'created_at']
        read_only_fields = ['follower'] 
class CreateFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']
        
    def create(self, validated_data):
        
        user = self.context['request'].user
        validated_data['follower'] = user
        return super().create(validated_data)

    