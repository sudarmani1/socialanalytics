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
