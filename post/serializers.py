from rest_framework import serializers
from .models import Post, PostComment
from user.serializers import UserBasicSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()

    class Meta:
        model = PostComment
        fields = '__all__'
