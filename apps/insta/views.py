from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .helpers import *
from InstagramAPI import InstagramAPI


# Create your views here.
@login_required
def index(request):
    username = ""
    password = ""
    data = {}

    api = instagram_login(username, password)
    try:
        if api.get('error'):
            data['error'] = api.get('error')
            return render(request,'1.html',data)
    except:
        pass

    following_users = get_insta_following_list(api)


    # follower_users = get_insta_followers_list(api)

    data['follower_users'] = following_users
    data['follower_count'] = len(following_users)


    return render(request,'1.html',data)