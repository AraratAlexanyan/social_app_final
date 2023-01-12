from django.contrib import admin
from post.models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'status',  'description', 'likes_count', 'saved_count')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass



