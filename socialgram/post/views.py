from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from socialgram.models import Posts
from .serializers import (PostCreateSerializer,
                          PostListViewSerializer,
                          PostGetViewSerializer,
                          PostDeleteViewSerializer)

#create the post view
class Post_create(generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostCreateSerializer

    def post(self, request):
        serializer_class = PostCreateSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Post_list(generics.GenericAPIView):
    # get the list of post
    queryset = Posts.objects.all()
    serializer_class = PostListViewSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = PostListViewSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


#get the single post update it using id by providing action to view or update
class Post_detail(generics.GenericAPIView):

    queryset = Posts.objects.all()
    serializer_class = PostGetViewSerializer

    def post(self, request):
        serializer_class = PostGetViewSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


#delete the post using id
class Post_delete(generics.GenericAPIView):
    # delete the post
    queryset = Posts.objects.all()
    serializer_class = PostDeleteViewSerializer

    def post(self, request):
        serializer_class = PostDeleteViewSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
