from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Follow


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:

        model = User
        fields = '__all__'

    def validate_password(self, value):

        return make_password(value)


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('favorite',)
