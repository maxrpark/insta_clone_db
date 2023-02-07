from django.urls import path
from .views import MyTokenObtainPairView, UpdateUserDetails

from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/my-profile-info/<str:id>',
         UpdateUserDetails.as_view(), name='my_profile_info'),

]
