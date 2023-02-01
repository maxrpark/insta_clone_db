from user.models import User
from datetime import timezone
from django.db import models
# Create your models here.


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    location = models.TextField(null=True,  default=None)
    upload_at = models.DateTimeField(auto_now=True)
    is_good = models.BooleanField(default=True)
    is_comment = models.BooleanField(default=True)
    goods = models.PositiveIntegerField(default=True)

    def publish(self):
        self.upload_at = timezone.now()
        self.save()

    def __str__(self):
        return self.content


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.TextField()


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    upload_at = models.DateTimeField(auto_now=True)


class PostCommentReply(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    upload_at = models.DateTimeField(auto_now=True)


class StoryPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField()
    upload_at = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_at = timezone.now()
        self.save()

    def __str__(self):
        return self.content
