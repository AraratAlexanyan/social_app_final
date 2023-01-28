from rest_framework import serializers

from post.models import Comment, Post
from user.serializer import UserSerializer, UserSerializerRepr


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('comment', 'post', 'author')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = data.pop("author")
        data["author"] = UserSerializerRepr(author).data

        return data


class PostModelSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ("id", "description", "status", "created_at",
                  'likes_count', 'likes', 'saves', 'saved_count', 'author')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = data.pop("author")
        data["author"] = UserSerializerRepr(author).data

        return data


class ListPostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ("created_at", "author", "description")
