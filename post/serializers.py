from rest_framework import serializers
from .models import Post
from user.serializers import UserBasicSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()

    class Meta:
        model = Post
        fields = '__all__'
