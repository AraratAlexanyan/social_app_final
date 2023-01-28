from post.models import Post

class Feed:
    def get_post_list(self, user):
        queryset = Post.objects.filter(author__favorite__follower_user=user).order_by('-created_at') \
            .select_related('author').prefetch_related('comments')

        print(queryset)
        return queryset

    def get_single_post(self, pk: int):
        return Post.objects.select_related('author').prefetch_related('comments').get(id=pk)


feed_service = Feed()
