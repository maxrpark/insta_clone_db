import cloudinary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework import status

# Create your views here.


class UploadImage(APIView):
    permission_classes = [AllowAny]  # TODO

    def post(self,  req):
        print(req.FILES)
        if 'file' not in req.FILES:
            return Response({
                'msg': "no \'file\' attached",
            }, status=status.HTTP_400_BAD_REQUEST)

        file = req.FILES['file']
        if file.content_type == 'image/jpeg' or file.content_type == 'image/png' or file.content_type == 'image/jpg':

            try:
                res = cloudinary.uploader.upload(req.FILES['file'],
                                                 folder="instagram_db",
                                                 #  public_id="my_dog",
                                                 #    overwrite=True,
                                                 resource_type="image"
                                                 )
                return Response({
                    'url': res['secure_url'],
                    'public_id': res['public_id'],
                })
            except Exception as e:
                return {'error': e}

        return Response({
            'msg': f" {file.content_type} Invalid format, valid formats are jpg/png/jpg",
        }, status=status.HTTP_400_BAD_REQUEST)


# author = models.ForeignKey(User, on_delete=models.CASCADE)
# content = models.TextField()
# location = models.TextField()
# upload_at = models.DateTimeField(auto_now=True)
# is_good = models.BooleanField()
# is_comment = models.BooleanField()
# goods = models.PositiveIntegerField()
class CreatePost(APIView):
    def post(self, req):
        values = ["author", "content", "location",
                  "upload_at", "is_good", "is_good", "goods"]
        for key in values:
            if req.data.get(key) is not None:
                pass
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': f"Please provide value for '{key}' value"})
        return Response(status=404,
                        data={'error': f"Please provide value for '{key}' value"})


class commentPost(APIView):
    def post(self, req):
        pass


class replyComment(APIView):
    def post(self, req):
        pass


class PostStory(APIView):
    def post(self, req):
        pass
# createPost
# postComment
# replyComment
# StoryPost
