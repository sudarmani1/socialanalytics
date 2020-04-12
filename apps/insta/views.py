from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import InstagramAnalytics

from .helpers import *

from InstagramAPI import InstagramAPI
from twilio.rest import Client

# Create your views here.
@login_required
def index(request):
    username = settings.INSTA_USERNAME
    password = settings.INSTA_PASSWORD
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


@csrf_exempt
def twilio(request):
    if request.method == 'POST':
        account_sid = settings.ACCOUNT_SID
        auth_token  = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)

        if request.POST.get('Body') == 'Hi':
            body = "[-] Welcome To Project SocAn [-] \n -Developed By D Ashwin"
        elif request.POST.get('Body') == 'help':
            body = "[-] Select command option [-] \n" \
                    "1) Get Insta Analytics \n" \
                    "2) Update/Sync Insta Analytics Data"
        elif request.POST.get('Body') == '1':
            body = get_insta_analytics()
        elif request.POST.get('Body') == '2':
            body = update_insta_analytics()
        else:
            body = "Invalid Choice... Please reply 'help' to see the option"

        message = client.messages.create(
                                      from_='whatsapp:+14Secreate',
                                      body=body,
                                      to='whatsapp:+91'
                                  )
        return HttpResponse("Done")
    else:
        return HttpResponse("GET")


