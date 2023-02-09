
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, insta_id, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, insta_id, password, **other_fields)

    def create_user(self, email, insta_id, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          insta_id=insta_id, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    user_name = models.CharField(max_length=150, blank=True)
    insta_id = models.CharField(max_length=255, unique=True)
    is_professional = models.BooleanField(default=False)

    followers = models.ManyToManyField(
        'User', related_name="user_followers", blank=True)

    following = models.ManyToManyField(
        'User', related_name="user_following", blank=True)

    profile_pic = models.TextField(blank=True, null=True)
    profile_name = models.TextField(blank=True, null=True)
    profile_website = models.TextField(blank=True, null=True)
    profile_info = models.TextField(blank=True, null=True)

    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'insta_id'
    REQUIRED_FIELDS = ['email']

    # def follow_user(self, follower):
    #     return self.following.add(follower)

    # def unfollow_user(self, to_unfollow):
    #     return self.following.remove(to_unfollow)

    def is_following(self, checkuser):
        return checkuser in self.following.all()

    # def get_number_of_followers(self):
    #     if self.followers.count():
    #         return self.followers.count()
    #     else:
    #         return 0

    # def get_number_of_following(self):
    #     if self.following.count():
    #         return self.following.count()
    #     else:
    #         return 0

    def __str__(self):
        return self.insta_id
