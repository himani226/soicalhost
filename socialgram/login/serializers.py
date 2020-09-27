from uuid import uuid4

from django.db.models import Q  # for queries
from django.core.exceptions import ValidationError
from django.contrib.auth import (authenticate, login, logout)

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from socialgram.models import UserProfileInfo
from socialgram.utility import authenticateUser, success_response, no_success_response


class UserSerializer(serializers.ModelSerializer):
    #user registration serializer
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfileInfo.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfileInfo.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    class Meta:
        model = UserProfileInfo
        exclude = ('ifLogged',)


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = UserProfileInfo.objects.filter(
                Q(email=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = UserProfileInfo.objects.get(email=user_id)
        else:
            #else username has been passed
            user = UserProfileInfo.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = UserProfileInfo.objects.get(username=user_id)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = UserProfileInfo
        fields = (
            'user_id',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    #User logout handler serializer using token
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        user = None
        #validate token
        status, user = authenticateUser(token)
        if status:
            user.ifLogged = False
            user.token = ""
            user.save()
            data = success_response()
            data['message'] = "User is logged out successfully"
            data['token'] = ""
            return data
        else:
            user['message'] = "Not a valid token found"
            user['token'] = ""
            return user

    class Meta:
        model = UserProfileInfo
        fields = (
            'status',
            'token',
            'message',
        )
