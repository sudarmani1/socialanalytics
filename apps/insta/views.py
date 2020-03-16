from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .helpers import *
from instagram.client import InstagramAPI

# Create your views here.
@login_required
def index(request):
    import pdb; pdb.set_trace()
    api = InstagramAPI("username", "password")
    api.login()
    api.searchUsername(username) #Gets most recent post from user
    result = api.LastJson
    username_id = result['user']['pk']
    user_posts = api.getUserFeed(username_id)
    result = api.LastJson
    media_id = result['items'][0]['id']

    api.getMediaLikers(media_id)
    users = api.LastJson['users']
    for user in users:
        users_list.append({'pk':user['pk'], 'username':user['username']})

    return render(request,'1.html',data)