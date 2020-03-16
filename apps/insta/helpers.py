import requests
from InstagramAPI import InstagramAPI


def get_token():
    response = requests.get('https://www.instagram.com/oauth/authorize/?client_id=8caca983cf3949ef81bc1dd3e1c3e847&redirect_uri=http://127.0.0.1:8000/insta&response_type=token')
    return response

def get_media(tkn):
    response = requests.get('https://api.instagram.com/v1/self/media/recent?access_token=2016904458.8caca98.d22a52c1337e4ad7b90ee1ee24a54c82'+tkn)
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