from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from post.models import Post

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'like_counts', 'favorites_count')

    def like_counts(self, obj):
        result = Post.objects.filter(likes=obj).count()
        return result

    def favorites_count(self, obj):
        result = Post.objects.filter(favorites=obj).count()
        return result
