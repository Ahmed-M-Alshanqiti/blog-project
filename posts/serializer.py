from rest_framework import serializers
from .models import Post, PostContent, Comment
import json

class PostContentSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField()
    media_file = serializers.FileField(required=False, allow_null=True)
    type = serializers.CharField(source='content_type')
    data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostContent
        fields = ['order', 'type', 'text_content', 'media_file', 'data']
        read_only_fields = ('post', 'data')

    def get_data(self, obj):
        if obj.content_type == 'text':
            return obj.text_content
        return None

class PostSerializer(serializers.ModelSerializer):
    content_blocks = PostContentSerializer(many=True, required=False)
    user_username = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    the_user_ho_liked_the_post = serializers.SerializerMethodField()
    how_meny_user_have_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'user_username', 'title', 'slug',
            'content_blocks', 'created_at', 'likes_count','the_user_ho_liked_the_post','how_meny_user_have_posts'
        ]
        read_only_fields = ('user', 'slug', 'created_at')

    def get_the_user_ho_liked_the_post(self,obj):
        return list(obj.likes.all().values_list('username', flat=True))

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_how_meny_user_have_posts(self,obj):
        return  list(obj.user.filter(user=obj.user))
    
    def create(self, validated_data):
        request = self.context.get('request')
        files = request.FILES

        content_blocks_data = validated_data.pop('content_blocks', [])
        if isinstance(content_blocks_data, str):
            content_blocks_data = json.loads(content_blocks_data)

        post = Post.objects.create(**validated_data)

        for block in content_blocks_data:
            if block.get('type') == 'text':
                PostContent.objects.create(post=post, **block)
                continue

            if block.get('type') == 'image':
                file_key = block.get('file_key')
                if file_key and file_key in files:
                    file = files[file_key]
                    PostContent.objects.create(
                        post=post,
                        order=block.get('order'),
                        content_type='image',
                        media_file=file
                    )

        return post

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_username', 'content', 'created_at']
        read_only_fields = ['user']
