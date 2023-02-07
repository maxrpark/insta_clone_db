import cloudinary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .permissions import IsPostOrIsAuthenticated, IsUserObjectOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import PostSerializer, PostCommentSerializer, ReplyCommentSerializer
from user.models import User
from .models import Post, PostComment, PostCommentReply


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


class UserPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req, pk):
        try:
            user = User.objects.get(pk=pk)
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)


class SinglePost(APIView):
    permission_classes = [IsUserObjectOrReadOnly]

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
            self.check_object_permissions(self.request, post)
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
            self.check_object_permissions(self.request, post)
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


class CreateComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):

        values = ["post_id", "content"]

        req_data = req.data
        missing = [
            value for value in values if value not in req_data.keys()]

        if missing:
            return Response({"message": f"The following keys are missing: {missing}"})

        user = User.objects.get(insta_id=req.user)

        if user is None:
            return Response({"message": "No user found"})
        try:
            post = Post.objects.filter(pk=req_data['post_id']).last()
            if user is None:
                return Response({"message": "No user found"})

            new_comment = PostComment(
                post=post,
                author=user,
                content=req_data['content']
            )

            new_comment.save()
            serializer = PostCommentSerializer(new_comment)

            return Response({"data": serializer.data})

        except Exception as e:
            return Response({"data": e})


class PostComments(APIView):
    permission_classes = [IsUserObjectOrReadOnly]

    def get(self, req, pk):
        try:
            post = Post.objects.get(pk=pk)
            comments = PostComment.objects.filter(post=post)
            serializer = PostCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def delete(self, req, pk):
        try:
            comments = PostComment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comments)
            comments.delete()

            return Response({"msg": "deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)


class PostStory(APIView):

    def post(self, req):
        pass


class ReplyComment(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req, pk):
        try:
            comment_reply = PostCommentReply.objects.filter(
                post_comment__pk=pk)

            serializer = ReplyCommentSerializer(comment_reply, many=True)

            return Response({"data": serializer.data})
        except:
            return Response({"msg": f"No post found with id {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, req, pk):
        values = ["content"]

        req_data = req.data
        missing = [
            value for value in values if value not in req_data.keys()]

        if missing:
            return Response({"message": f"The following keys are missing: {missing}"})
        try:
            user = User.objects.get(insta_id=req.user)

            if user is None:
                return Response({"message": "No user found"})
            post_comment = PostComment.objects.get(pk=pk)

            comment_reply = PostCommentReply(
                post_comment=post_comment,
                author=user,
                content=req_data['content']
            )
            comment_reply.save()

            serializer = ReplyCommentSerializer(comment_reply)

            return Response({"data": serializer.data})

        except Exception as e:
            return Response({"data": e})

    def delete(self, req, pk):
        try:
            reply_comment = PostCommentReply.objects.filter(pk=pk).last()
            if reply_comment is None:
                return Response({"message": "Not found"})

            if req.user.is_anonymous:
                return Response({"message": "No user found"})

            if reply_comment.author != req.user:
                return Response({"msg": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"msg": "deleted"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"data": e})
