from django.contrib import admin
from .models import InstagramUserAnalytics, TrackFollower, InstagramFollowing, InstagramFollower

# Register your models here.
admin.site.register(InstagramUserAnalytics)
admin.site.register(InstagramFollowing)
admin.site.register(InstagramFollower)
admin.site.register(TrackFollower)