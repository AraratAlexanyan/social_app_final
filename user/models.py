from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Follow(models.Model):
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    favorite_user = models.ForeignKey(User, related_name='favorite', on_delete=models.CASCADE, blank=True, default=None)
    followers_count = models.IntegerField(default=0)
    followed_date = models.DateTimeField(auto_now_add=True)


