from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from socialgram.models import UserProfileInfo
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer

class Register(generics.ListCreateAPIView):
    # get and post method
    queryset = UserProfileInfo.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method
    queryset = UserProfileInfo.objects.all()
    serializer_class = UserLoginSerializer

    #post method to post username and pasword
    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    #get method
    queryset = UserProfileInfo.objects.all()
    serializer_class = UserLogoutSerializer

    #post method to post token
    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)