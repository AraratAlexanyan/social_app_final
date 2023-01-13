from django.contrib.auth.models import User
from django.db import models

# Create your models here.


STATUS_CHOICES = (
    (0, "Creating"),
    (1, "Published"))


class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True, default='Category waiting for description')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_name = models.CharField(max_length=50, blank=True)
    description = models.TextField(null=True, blank=True, default='Post waiting for description')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='categories')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    likes_count = models.IntegerField(default=0)
    saves = models.ManyToManyField(User, related_name='favorites', blank=True, default=None)
    saved_count = models.IntegerField(default=0)

    def __str__(self):
        return self.author

    def save(
        self, *args, **kwargs
    ):
        self.likes_count = self.likes.count()
        self.saved_count = self.saves.count()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment[:10]+'...'


