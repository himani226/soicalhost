from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from socialgram.models import UserProfileInfo, Tags
from .serializers import (TagCreateSerializer,
                          TagViewListSerializer,
                          TagGetSerializer,
                          TagDeleteSerializer,)


class Tag_create(generics.GenericAPIView):
    # get all the tag values from the Tags database
    queryset = Tags.objects.all()
    serializer_class = TagCreateSerializer

    # post the tag value into the database
    def post(self, request, *args, **kwargs):
        serializer_class = TagCreateSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Tag_list(generics.GenericAPIView):
    # get the list of all tags created by user
    queryset = Tags.objects.all()
    serializer_class = TagViewListSerializer

    # post the tag value into the database
    def post(self, request, *args, **kwargs):
        serializer_class = TagViewListSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Tag_detail(generics.GenericAPIView):
    # update and view the tags using the id and write action as view or update
    queryset = Tags.objects.all()
    serializer_class = TagGetSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = TagGetSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Tag_delete(generics.GenericAPIView):
    # delete the tags using the id
    queryset = Tags.objects.all()
    serializer_class = TagDeleteSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = TagDeleteSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)