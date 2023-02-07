from rest_framework import serializers
from .models import Post, PostComment, PostCommentReply, Images
from user.serializers import UserBasicSerializer


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class UserProfilePostSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()
    post_images = ImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()

    class Meta:
        model = PostComment
        fields = '__all__'


class ReplyCommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer()

    class Meta:
        model = PostCommentReply
        fields = '__all__'
