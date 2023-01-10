from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from post.models import Category, Comment, Post, Follow
from post.serializers import CategorySerializer, CommentSerializer, PostModelSerializer, FollowSerializer
from post.post_search import PostFilter


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CommentsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req):
        data = Comment.objects.all()
        serializer = CommentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = CommentSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=req.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req):
        data = Post.objects.all()
        filtered = PostFilter(req.GET, data)
        serializer = PostModelSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, req):
        serializer = PostModelSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):

    def get(self, req, pk):
        data = Post.objects.get(pk=pk)
        comments = data.comment_set.all()
        post_serializer = PostModelSerializer(data)
        comment_serializer = CommentSerializer(comments, many=True)

        return Response({'post': post_serializer.data, 'comments': comment_serializer.data})


class FollowApiView(APIView):
    def get(self, req):

        data = Follow.objects.filter(follower=req.user)
        serializer = FollowSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, req):

        follows = Follow.objects.filter(follower=req.user).filter(favorite=req.data['favorite'])

        if not follows:
            serializer = FollowSerializer(data=req.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(follower=req.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            follows.delete()
            return Response(status=status.HTTP_200_OK)


class PostLikesAPIView(APIView):

    def post(self, req, pk):

        post = Post.objects.get(pk=pk)
        is_liked = False

        for like in post.likes.all():
            if like == req.user:
                is_liked = True

        if not is_liked:
            post.likes.add(req.user)
            post.save()

        if is_liked:
            post.likes.remove(req.user)
            post.save()

        return Response(status=status.HTTP_200_OK)


class PostSavesAPIView(APIView):

    def post(self, req, pk):

        post = Post.objects.get(pk=pk)
        is_favorite = False

        for saved in post.favorites.all():
            if saved == req.user:
                is_favorite = True

        if not is_favorite:
            post.favorites.add(req.user)
            post.save()

        if is_favorite:
            post.favorites.remove(req.user)
            post.save()

        return Response(status=status.HTTP_200_OK)
