import requests
from InstagramAPI import InstagramAPI
from .models import InstagramUserAnalytics, LinkedFbInfo, InstagramFollowing, InstagramFollower
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

def create_insta_following_list():
    username = settings.INSTA_USERNAME
    password = settings.INSTA_PASSWORD

    api = instagram_login(username, password)
    try:
        if api.get('error'):
            return api.get('error')
    except:
        pass
    api.getSelfUsersFollowing()
    result = api.LastJson
    count = 0
    for user in result['users']:
        count += 1
        InstagramFollowing.objects.create(
            user_id = 1,
            insta_pk        = user['pk'],
            insta_username  = user['username'],
            insta_full_name = user['full_name'],
            is_private      = user['is_private'],
            profile_pic_url = user['profile_pic_url'],
            is_verified     = user['is_verified'])

    print("Total {} objects created.",format(count))
    return True


def create_insta_follower_list():
    username = settings.INSTA_USERNAME
    password = settings.INSTA_PASSWORD

    api = instagram_login(username, password)
    try:
        if api.get('error'):
            return api.get('error')
    except Exception as e:
        print(str(e))


    api.getSelfUserFollowers()
    result = api.LastJson
    count = 0
    for user in result['users']:
        count += 1
        InstagramFollower.objects.create(
            user_id = 1,
            insta_pk        = user['pk'],
            insta_username  = user['username'],
            insta_full_name = user['full_name'],
            is_private      = user['is_private'],
            profile_pic_url = user['profile_pic_url'],
            is_verified     = user['is_verified'])

    print("Total {} objects created.".format(count))
    return True

def get_insta_analytics():
    data = {}
    insta_ana = InstagramUserAnalytics.objects.all().last()

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
        full_name       = result['user']['full_name']
        profile_pic_url = result['user']['profile_pic_url']
        followers       = result['user']['follower_count']
        following       = result['user']['following_count']
        media_count     = result['user']['media_count']

        insta_pk        = result['user']['pk']
        insta_uname     = result['user']['username']
        profile_pic_url = result['user']['profile_pic_url']
        profile_pic_id  = result['user']['profile_pic_id']
        biography       = result['user']['biography']
        is_private      = result['user']['is_private']

        profile_pic_320 = result['user']['hd_profile_pic_versions'][0]['url']
        profile_pic_640 = result['user']['hd_profile_pic_versions'][1]['url']
        profile_pic_full= result['user']['hd_profile_pic_url_info']['url']


        fb_id      = result['user']['linked_fb_info']['linked_fb_user']['id']
        fb_name    = result['user']['linked_fb_info']['linked_fb_user']['name']
        fb_valid   = result['user']['linked_fb_info']['linked_fb_user']['is_valid']

        # Create FB LinkedFbInfo
        linked_fb = LinkedFbInfo.objects.create(
            fb_id   = fb_id,
            name    = fb_name,
            is_valid= fb_valid)

        InstagramUserAnalytics.objects.create(
            user_id  = 1, 
            linked_fb_info = linked_fb,
            total_followers = followers,
            total_following = following,
            total_likes_get = 1,
            total_liked     = 1,
            media_count     = media_count,
            insta_pk        = insta_pk,
            insta_full_name = full_name,
            insta_username  = insta_uname,
            profile_pic_url = profile_pic_url,
            profile_pic_id  = profile_pic_id,
            is_private      = is_private,
            biography       = biography,
            hd_profile_pic_versions_320 = profile_pic_320,
            hd_profile_pic_versions_640 = profile_pic_640,
            hd_profile_pic_url_info = profile_pic_full
        )
        return "Successfully Synched"
    except Exception as e:
        print(str(e))
        return "There is some issue while syncing your Insta data. Error : " + str(e)

def get_a_follwer_data():
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
        InstagramUserAnalytics.objects.create(
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