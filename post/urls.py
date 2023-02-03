from django.urls import path
from .views import UploadImage, PostView, SinglePost, CreateComment, PostComments


urlpatterns = [
    path('', PostView.as_view(),  name='create_post'),
    path('image-upload/', UploadImage.as_view(),  name='image_upload'),
    path('<str:pk>', SinglePost.as_view(),  name='single_post'),
    path('comments/', CreateComment.as_view(),  name='create_comment'),
    path('comments/<str:pk>', PostComments.as_view(),  name='post_comments'),
]
