from django.db import models
from django.contrib.auth.models import User

# Create your models here.


'''
    total_followers
    total_following
    total_likes_get
    total_liked
    last_updated_at
'''
class InstagramAnalytics(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    total_followers = models.IntegerField()
    total_following = models.IntegerField()
    total_likes_get = models.IntegerField()
    total_liked     = models.IntegerField()
    media_count     = models.IntegerField(default=0)
    last_updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.pk)