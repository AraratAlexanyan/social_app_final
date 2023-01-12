from django.contrib.auth.models import User, AbstractUser
from django.db import models

#  Petqe havaqel user follow count ccuyc tvox funkcia
# class NewUser(AbstractUser):
#
#     def save(
#             self, *args, **kwargs
#     ):
#         self.followers_count = self.follower.count()
#         self.following_count = self.followung.count()
#         super(User, self).save(*args, **kwargs)
#

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    favorite = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_user')

    def __str__(self):
        return str(self.follower)
