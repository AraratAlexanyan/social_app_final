from .services import feed_service
from rest_framework import viewsets, permissions, response

from post.serializers import ListPostSerializer, PostModelSerializer


class FeedView(viewsets.GenericViewSet):
    """ View follower`s feed
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = feed_service.get_post_list(request.user)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = feed_service.get_single_post(kwargs.get('pk'))
        serializer = PostModelSerializer(instance)
        return response.Response(serializer.data)
