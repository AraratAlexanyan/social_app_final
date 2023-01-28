from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.filters.post_filters import PostFilter
from post.models import Comment, Post
from post.serializers import CommentSerializer, PostModelSerializer


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

        is_self = req.GET.get('q') == 'my_posts'
        if is_self:
            data = Post.objects.filter(author=req.user)
            print(data)
            filtered = PostFilter(req.GET, data)
            serializer = PostModelSerializer(filtered.qs, many=True)
            return Response(serializer.data)
        else:
            print('/'*15)

            data = Post.objects.all()
            serializer = PostModelSerializer(data, many=True)

            return Response(serializer.data)

    def post(self, req):
        serializer = PostModelSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=req.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):

    def get(self, req, pk):
        data = Post.objects.get(pk=pk)
        comments = data.comment_set.all()
        post_serializer = PostModelSerializer(data)
        comment_serializer = CommentSerializer(comments, many=True)

        return Response({'post': post_serializer.data, 'comments': comment_serializer.data})


class PostLikesAPIView(APIView):

    def post(self, req, pk):

        print('print')

        post = Post.objects.get(pk=pk)
        is_liked = False

        for like in post.likes.all():
            if like == req.user:
                is_liked = True
                break

        if not is_liked:
            post.likes.add(req.user)
            post.likes_count = post.likes.all().count()
            post.save()

        if is_liked:
            post.likes.remove(req.user)
            post.likes_count = post.likes.all().count()
            post.save()

        return Response(status=status.HTTP_200_OK)


class PostSavesAPIView(APIView):

    def post(self, req, pk):

        post = Post.objects.get(pk=pk)
        is_favorite = False

        for saved in post.saves.all():
            if saved == req.user:
                is_favorite = True

        if not is_favorite:
            post.saves.add(req.user)
            post.saved_count = post.saves.all().count()
            post.save()

        if is_favorite:
            post.saves.remove(req.user)
            post.saved_count = post.saves.all().count()
            post.save()

        return Response(status=status.HTTP_200_OK)
