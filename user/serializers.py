from rest_framework import serializers
from .models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('insta_id', "profile_pic")
