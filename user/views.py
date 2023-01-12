from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from itsdangerous import URLSafeTimedSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import Follow
from user.serializer import UserSerializer, FollowSerializer


class UserLists(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, req):

        model = User.objects.all()
        serializer = UserSerializer(model, many=True)

        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req, pk):
        model = User.objects.get(pk=pk)
        serializer = UserSerializer(model)
        follower = Follow.objects.filter(follower=req.user)
        x = follower.count()
        print(x)
        return Response({'user': serializer.data, 'followers count': x})


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
        user.save()

        return Response('Account successfully verified', status=status.HTTP_204_NO_CONTENT)


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

