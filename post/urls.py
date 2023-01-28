from django.urls import path

from post.views import *

urlpatterns = [
    path('comm/', CommentsListView.as_view()),
    path('post/', PostApiView.as_view()),
    path('post/<int:pk>/', PostDetailView.as_view()),
    path('post/like/<int:pk>/', PostLikesAPIView.as_view()),
    path('post/fav/<int:pk>/', PostSavesAPIView.as_view()),

]
