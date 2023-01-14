from django.db.models import Q
from django_filters import rest_framework as filters
from post.models import Post


class PostFilter(filters.FilterSet):
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    q_str = filters.CharFilter(method='post_name_desc')

    class Meta:
        model = Post
        fields = ['description']

    def post_name_desc(self, qs, name, value):
        new_qs = qs.filter(Q(description__icontains=value))
        return new_qs

    def category_name(self, qs, name, value):
        return qs.filter(category__name__icontains=value)
