from django.contrib import admin
from .models import Post, PostComment,  PostCommentReply, StoryPost, Images


admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostCommentReply)
admin.site.register(StoryPost)
admin.site.register(Images)
