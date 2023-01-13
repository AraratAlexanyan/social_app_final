from django.urls import path

from user.views import UserCreate, UserLists, UserVerify, UserDetailView, FollowApiView

urlpatterns = [
    path('', UserLists.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('reg/', UserCreate.as_view()),
    path('verify_token/', UserVerify.as_view()),
    path('follow/', FollowApiView.as_view()),
    path('follow/<int:pk>/', FollowApiView.as_view()),
]
