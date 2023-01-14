from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Follow


# from user.models import Follow
#

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:

        model = User
        fields = '__all__'


class UserPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


# class UserFollowsSerializer(serializers.ModelSerializer):
#
#     new_user = serializers.ReadOnlyField()
#
#     class Meta:
#         model = NewUser
#         fields = ('follows', 'new_user')

class FollowSerializer(serializers.ModelSerializer):
    followed_date = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()

    class Meta:
        model = Follow
        fields = '__all__'
