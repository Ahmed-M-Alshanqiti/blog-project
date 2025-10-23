from rest_framework import  generics, status,mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Follow
from ..serializers import UserSerializer, FollowSerializer , FollowerSerializer, CreateFollowSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model 

CustomUser = get_user_model() 


class Login_to_web_site():
    permission_classes = [all]


class FollowerShow(
    mixins.ListModelMixin,            
    mixins.CreateModelMixin,          
    generics.GenericAPIView           
):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateFollowSerializer
        return FollowerSerializer

    def get_queryset(self):

        if self.request.method == 'GET':
            return Follow.objects.filter(following=self.request.user)
        
        return Follow.objects.all()

    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)

class FollowView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        target_id = request.data.get("following")
        if not target_id:
            return Response({"error": "Missing 'following' id"}, status=400)

        if request.user.id == int(target_id):
            return Response({"error": "Cannot follow yourself"}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following_id=target_id
        )
        if not created:
            follow.delete()
            return Response({"message": "Unfollowed"}, status=200)
        return Response({"message": "Followed"}, status=201)

@api_view(['GET'])
def get_user_profile (request, **kwargs):
    userName = kwargs.get('username', None)
    id = kwargs.get('id', None)

    try:
        if userName:
            user_instance = CustomUser.objects.get(username=userName)
        else:    
             user_instance = CustomUser.objects.get(id=id) 
        
    except CustomUser.DoesNotExist: 
        return Response({"error": f"User with ID {id} not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user_instance)
    
    return Response(serializer.data, status=status.HTTP_200_OK)