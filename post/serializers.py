from rest_framework import serializers

from post.models import Category, Comment, Post


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    # author = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('comment', 'post')


class PostModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "description", "status", "created_at",
                  "category", 'likes_count', 'likes', 'saves', 'saved_count')



