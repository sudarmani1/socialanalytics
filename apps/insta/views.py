from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import InstagramUserAnalytics

from .helpers import *

from InstagramAPI import InstagramAPI
from twilio.rest import Client
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.loader import get_template
from django.core.mail import EmailMessage

# Create your views here.
@login_required
def index(request):
    data = {}
    # update_insta_analytics()

    data['notifications'] =Notification.objects.filter(is_read=False)
    data['analytics'] = InstagramUserAnalytics.objects.filter(user=request.user).last()
    return render(request,'insta/my_insta_dashbaord.html',data)

@login_required
def update_insta_feed(request):
    try:
        # update_insta_analytics()
        pass
        return JsonResponse({'status':True,'message':'Successfully Updated!'})
    except Exception as e:
        return JsonResponse({'status':False,'message':str(e)})

@login_required
def insta_follower_list(request):
    data = {}

    # create_insta_follower_list()
    follower_user = InstagramFollower.objects.filter(user=request.user)
    data['private_profile_count'] = follower_user.filter(is_private = True).count()
    data['verified_profile_count'] = follower_user.filter(is_verified = True).count()
    data['follower_user_count'] = follower_user.count()

    page = request.GET.get('page', 1)

    paginator = Paginator(follower_user, 10)
    try:
        follower_user = paginator.page(page)
    except PageNotAnInteger:
        follower_user = paginator.page(1)
    except EmptyPage:
        follower_user = paginator.page(paginator.num_pages)

    data['follower_user'] = follower_user
    return render(request,'insta/insta_followers.html',data)


@login_required
def insta_following_list(request):
    data = {}
    # create_insta_following_list()

    following_user = InstagramFollowing.objects.filter(user=request.user)
    data['private_profile_count'] = following_user.filter(is_private = True).count()
    data['verified_profile_count'] = following_user.filter(is_verified = True).count()
    data['following_user_count'] = following_user.count()

    page = request.GET.get('page', 1)

    paginator = Paginator(following_user, 10)
    try:
        following_user = paginator.page(page)
    except PageNotAnInteger:
        following_user = paginator.page(1)
    except EmptyPage:
        following_user = paginator.page(paginator.num_pages)

    data['following_user'] = following_user
    return render(request,'insta/insta_following.html',data)


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


def sendmail(request):
    try:
        ctx = {
            "schedule_type"        : "test"
        }

        subject = "demo"

        message = get_template('email/demo.html').render(ctx)
        msg = EmailMessage(subject, message, to=('kewef44103@katamo1.com',),from_email='kewef44103@katamo1.com')
        msg.content_subtype = 'html'
        msg.send()
        print("Mail Sent Successfully")
        return HttpResponse("Sent mail")
    except Exception as e:
        print("Uh oh, We met error :",str(e))