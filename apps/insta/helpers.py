import requests
from InstagramAPI import InstagramAPI
from .models import InstagramAnalytics
from django.conf import settings


def get_token():
    response = requests.get('https://www.instagram.com/oauth/authorize/?client_id=123&redirect_uri=http://127.0.0.1:8000/insta&response_type=token')
    return response

def get_media(tkn):
    response = requests.get('https://api.instagram.com/v1/self/media/recent?access_token=2016904458.123.123'+tkn)
    return response

def instagram_login(username, password):
    try:
        api = InstagramAPI(username, password)
        res = api.login()
        if res:
            return api
        else:
            return {"error" : "Invalid credentials"}
    except:
        return {"error" : "Invalid credentials"}

def get_insta_followers_list(api):
    follower_users = []
    api.getSelfUserFollowers()
    result = api.LastJson
    for user in result['users']:
        follower_users.append({'pk':user['pk'], 'username':user['username']})
    return follower_users

def get_insta_following_list(api):
    following_users = []
    api.getSelfUsersFollowing() # Get users which you are following
    result = api.LastJson
    for user in result['users']:
        following_users.append({'pk':user['pk'], 'username':user['username']})
    return following_users

def get_insta_analytics():
    data = {}
    insta_ana = InstagramAnalytics.objects.all().last()

    data['Total Followers'] = insta_ana.total_followers
    data['Total Following'] = insta_ana.total_following
    data['Total Likes Get'] = insta_ana.total_likes_get
    data['Total Liked']     = insta_ana.total_liked
    data['Total Media Count']     = insta_ana.media_count
    data['Last Updated_at'] = insta_ana.last_updated_at.strftime("%d/%m/%Y, %H:%M:%S")

    return str(data)

def update_insta_analytics():
    try:
        username = settings.INSTA_USERNAME
        password = settings.INSTA_PASSWORD

        api = instagram_login(username, password)
        try:
            if api.get('error'):
                return api.get('error')
        except:
            pass

        api.getSelfUsernameInfo()
        result = api.LastJson
        username = result['user']['username']
        full_name = result['user']['full_name']
        profile_pic_url = result['user']['profile_pic_url']
        followers = result['user']['follower_count']
        following = result['user']['following_count']
        media_count = result['user']['media_count']
        
        # Create New Object
        InstagramAnalytics.objects.create(
            user_id  = 1, 
            total_followers = followers,
            total_following = following,
            media_count = media_count,
            total_likes_get = 1,
            total_liked =1)

        return "Successfully Synched"
    except Exception as e:
        print(str(e))
        return "There is some issue while syncing your Insta data. Error : " + str(e)