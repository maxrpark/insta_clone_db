import cloudinary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .permissions import IsPostOrIsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import PostSerializer
from user.models import User
from .models import Post, PostComment


class UploadImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,  req):
        user = User.objects.get(insta_id=req.user)
        if 'file' not in req.FILES:
            return Response({
                'msg': "no \'file\' attached",
            }, status=status.HTTP_400_BAD_REQUEST)

        file = req.FILES['file']
        if file.content_type == 'image/jpeg' or file.content_type == 'image/png' or file.content_type == 'image/jpg':

            try:
                res = cloudinary.uploader.upload(req.FILES['file'],
                                                 folder=f"instagram_db/{user.insta_id}",
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


class PostView(APIView):
    permission_classes = [IsPostOrIsAuthenticated]

    def get(self, req):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def post(self, req):
        values = ["content", "location",
                  "is_good", "is_good"]

        req_data = req.data
        missing = [value for value in values if value not in req_data.keys()]

        if missing:
            return Response({"message": f"The following keys are missing: {missing}"})

        user = User.objects.get(insta_id=req.user)
        if user is None:
            return Response({"message": "No user found"})
        try:

            new_post = Post(
                author=user,
                content=req_data['content'],
                location=req_data['location'],
                is_good=req_data['is_good'],
                is_comment=req_data['is_comment'],
            )

            new_post.save()
            serializer = PostSerializer(new_post)

            return Response({"data": serializer.data})
        except Exception as e:
            return Response({"data": e})


class commentPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):

        values = ["post", "author", "content"]

        req_data = req.data
        missing = [
            value for value in values if value not in req_data.keys()]

        if missing:
            return Response({"message": f"The following keys are missing: {missing}"})

        user = User.objects.get(insta_id=req.user)
        if user is None:
            return Response({"message": "No user found"})
        post = Post.objects.filter(pk=req_data['id']).last()
        if user is None:
            return Response({"message": "No user found"})

        new_post = PostComment(
            post=post,
            author=user,
            content=req_data['content']
        )
    # post
    # author
    # content


class replyComment(APIView):
    def post(self, req):
        pass


class PostStory(APIView):
    def post(self, req):
        pass
# postComment
# replyComment
# StoryPost


# SinglePost

class SinglePost(APIView):
    permission_classes = [IsPostOrIsAuthenticated]

    def get(self, req, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({"msg": "deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, req, pk):

        values = ["content", "location",
                  "is_good", "is_good"]

        req_data = req.data
        missing = [value for value in values if value not in req_data.keys()]

        if missing:
            return Response({"message": f"The following keys are missing: {missing}"})
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data={
                'content': req_data['content'],
                'location': req_data['location'],
                'is_good': req_data['is_good'],
                'is_comment': req_data['is_comment'],
            },  partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)
