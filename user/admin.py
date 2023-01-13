from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from user.models import Follow

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email',) #'followers_count', 'following_count', avelacnel count cuyc tvox funkcianer


# @admin.register(Follow)
# class FollowAdmin(admin.ModelAdmin):
#     list_display = ('follower', 'favorite')
