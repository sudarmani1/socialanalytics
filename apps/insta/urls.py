from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='insta-index'),
    path('insta-followers', views.insta_follower_list, name='insta-followers'),
    path('insta-following', views.insta_following_list, name='insta-following'),
    path('twilio', views.twilio, name='twilio'),
]