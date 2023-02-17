from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsUserObjectOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserBasicSerializer

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['insta_id'] = user.insta_id
        token['profile_pic'] = user.profile_pic
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UpdateUserDetails(APIView):
    permission_classes = [IsUserObjectOrReadOnly]

    def get(self, req, insta_id):
        user = User.objects.filter(insta_id=insta_id).last()
        if user is None:
            return Response({'msg': 'No user found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserBasicSerializer(user)
        return Response({'user': serializer.data})

    def patch(self, req, insta_id):
        user = User.objects.filter(insta_id=insta_id).last()
        if user is None:
            return Response({'msg': 'No user found'}, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(self.request, user)
        req_data = req.data

        data = {
            "insta_id": req_data['insta_id'],
            "profile_name": req_data['profile_name'],
            "profile_website": req_data['profile_website'],
            "profile_info": req_data['profile_info']
        },
        serializer = UserBasicSerializer(user, data=data[0], partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data})
        else:
            return Response({'errors': serializer.errors})
