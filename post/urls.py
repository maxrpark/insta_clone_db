from django.urls import path
from .views import UploadImage, PostView, SinglePost


urlpatterns = [
    path('', PostView.as_view(),  name='create_post'),
    path('image-upload/', UploadImage.as_view(),  name='image_upload'),
    path('<str:pk>', SinglePost.as_view(),  name='single_post'),
]
