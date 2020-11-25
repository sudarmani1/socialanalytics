from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
