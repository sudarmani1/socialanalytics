from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.insta.helpers import update_insta_analytics


class DemoApiView(APIView):
    def get(self, request):
        data = {"message": "hello world"}
        return Response(data, status=status.HTTP_200_OK)


class UpdateInsta(APIView):
    def get(self, request):
        update_insta_analytics()
        data = {"message": "hello world"}
        return Response(data, status=status.HTTP_200_OK)


class StalkInstaView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        import requests
        from bs4 import BeautifulSoup
        endpoint = "https://instadp.org/"
        data = {"username":username}
        res= requests.post(endpoint, data)
        soup = BeautifulSoup(res.text, "html.parser")
        data = soup.find_all('div', class_='container')
        a_class = data[0].find_all('a')
        url_ = a_class[0].get('href')
        return Response({"image_url": url_}, status=status.HTTP_200_OK)
