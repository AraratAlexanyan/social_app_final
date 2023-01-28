from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from itsdangerous import URLSafeTimedSerializer
from rest_framework import status
from rest_framework  import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import Follow
from user.serializer import UserSerializer, FollowSerializer, UserUpdateSerializer


class UserLists(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, req):

        model = User.objects.all()
        serializer = UserSerializer(model, many=True)

        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, req, pk):
        user = User.objects.get(id=pk)
        followers_count = user.favorite.count()
        serializer = UserSerializer(user)
        data = {'user_detail': serializer.data, 'followers_count': followers_count}
        return Response(data)


class UserUpdateView(ModelViewSet):
    """
        Edit user
    """
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserCreate(APIView):

    def post(self, req):

        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=False)

        tokenizer = URLSafeTimedSerializer(settings.SECRET_KEY)
        serialized_token = tokenizer.dumps({
            'email': serializer.data['email'],
            'username': serializer.data['username']
        })

        verify_url = f'{settings.BASE_URL}/user/verify_token?token={serialized_token}'

        send_mail(
            'Verification',
            'Verify your email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[serializer.data['email']],
            html_message=f'<a href={verify_url}>Click to verify email</a>'
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserVerify(APIView):
    def get(self, req):

        token = req.GET.get('token')
        tokenizer = URLSafeTimedSerializer(settings.SECRET_KEY)
        dat = tokenizer.loads(token, max_age=settings.VERIFICATION_TIME_IN_SECONDS)
        user = User.objects.get(username=dat['username'], email=dat['email'])
        user.is_active = True
        user.email = dat['email']
        user.save()

        return Response('Account successfully verified', status=status.HTTP_204_NO_CONTENT)


class FollowApiView(APIView):
    def get(self, req):

        data = Follow.objects.filter(follower_user=req.user)
        serializer = FollowSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, req, pk):

        follows = Follow.objects.filter(follower_user=req.user.id).filter(favorite_user=pk)

        if not follows:
            follow = Follow.objects.create(follower_user=req.user, favorite_user_id=pk)
            user = User.objects.get(id=pk)
            follow.followers_count = user.favorite.count()
            follow.save()
            return Response(follow)
        else:
            follows.delete()
            return Response(status=status.HTTP_200_OK)

