from rest_framework import serializers
from .models import User


class UserBasicSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('insta_id', "profile_pic",
                  "profile_name",
                  "profile_website",
                  "profile_info", "followers_count", 'following_count'
                  )

    def get_followers_count(self, obj):
        return obj.followers.all().count()

    def get_following_count(self, obj):
        return obj.following.all().count()
