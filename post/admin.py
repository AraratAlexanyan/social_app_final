from django.contrib import admin
from post.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'status',  'description', 'likes_count', 'saved_count', 'id')
    search_fields = ('author', 'status', 'description', )
    list_display_links = ('author', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', )



