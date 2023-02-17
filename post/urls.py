from django.urls import path
from .views import UploadImage, PostView, SinglePost, CreateComment, PostComments, ReplyComment, UserPosts, UserReels, UserFeeds


urlpatterns = [
    path('', PostView.as_view(),  name='create_post'),
    path('image-upload/', UploadImage.as_view(),  name='image_upload'),
    path('user/feeds/', UserFeeds.as_view(),  name='user_feeds'),
    path('<str:pk>', SinglePost.as_view(),  name='single_post'),
    path('user/<str:pk>/', UserPosts.as_view(),  name='user_posts'),
    path('user/reels/<str:pk>/', UserReels.as_view(),  name='user_posts'),


    ##
    path('comments/', CreateComment.as_view(),  name='create_comment'),
    path('comments/<str:pk>', PostComments.as_view(),  name='post_comments'),

    ##
    path('comments/reply/<str:pk>/', ReplyComment.as_view(),  name='reply_comment'),

]
