from django_filters import rest_framework as filter
from post.models import Post


class PostFilter(filter.FilterSet):
    post_name = filter.CharFilter(field_name="post_name", lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["post_name"]
