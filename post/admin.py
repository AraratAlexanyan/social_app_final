from django.contrib import admin
from post.models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'status',  'description', 'likes_count', 'saved_count')
    search_fields = ('author', 'status', 'description', )
    list_display_links = ('author', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', )



