from django.contrib.auth.models import User
from django.db import models

# Create your models here.


STATUS_CHOICES = (
    (0, "Creating"),
    (1, "Published"))


class Post(models.Model):
    description = models.TextField(null=True, blank=True, default='Post waiting for description')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    likes = models.ManyToManyField(User, blank=True, related_name='likes', default=None)
    likes_count = models.IntegerField(default=0)
    saves = models.ManyToManyField(User, related_name='favorites', blank=True, default=None)
    saved_count = models.IntegerField(default=0)

    def __str__(self):
        return self.description[:10] + '...'


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments",)

    def __str__(self):
        return self.comment[:10] + '...'
