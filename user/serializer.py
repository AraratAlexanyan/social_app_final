from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:

        model = User
        fields = '__all__'

    def validate_password(self, value):

        return make_password(value)
