import requests


def get_token():
    response = requests.get('https://www.instagram.com/oauth/authorize/?client_id=8caca983cf3949ef81bc1dd3e1c3e847&redirect_uri=http://127.0.0.1:8000/insta&response_type=token')
    return response


    
def get_media(tkn):
    response = requests.get('https://api.instagram.com/v1/self/media/recent?access_token=2016904458.8caca98.d22a52c1337e4ad7b90ee1ee24a54c82'+tkn)
    import pdb; pdb.set_trace()
    return response