from django.db import IntegrityError
from rest_framework import serializers
from socialgram.models import Tags
from socialgram.utility import authenticateUser, success_response, no_success_response


# create the tag and save into database
class TagCreateSerializer(serializers.ModelSerializer):
    tag_string = serializers.CharField(max_length=30,
                                       required=True)
    token = serializers.CharField(required=True)
    status = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        tag_string = data.get("tag_string", None)
        token = data.get("token", None)
        # validate user
        status, user = authenticateUser(token)
        if status:
            tag = Tags()
            try:
                tag.create(tag_string=tag_string, user=user)
                response = success_response()
                response['message'] = "Tags has been saved successfully"
            except IntegrityError:
                response = no_success_response()
                response['message'] = "Tag '%s' already exists" % (tag_string)
        else:
            response = user
            response['token'] = token
        response['tag_string'] = tag_string
        response['token'] = token
        return response

    class Meta:
        model = Tags
        fields = (
            'tag_string',
            'token',
            'status',
            'message',
        )


# view all the tags of user in database
class TagViewListSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    message = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    results = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        status, user = authenticateUser(token)
        if status:
            tags = []
            for p in Tags.objects.filter(created_by=user):
                tags.append(p.embed())
            response = success_response()
            response['results'] = tags
        else:
            response = no_success_response()
            response['message'] = "Login into the account to view Tag List"
        response['token'] = token
        return response

    class Meta:
        model = Tags
        fields = (
            'token',
            'message',
            'status',
            'results')


# view and update the list of tags
class TagGetSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    action = serializers.CharField(required=False)
    id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    tag_string = serializers.CharField(required=False)

    def validate(self, data):
        token = data.get("token", None)
        id = data.get("id", None)
        action = data.get("action", "view")
        status, user = authenticateUser(token)
        if status:
            tag = Tags.objects.filter(id=id, created_by=user).first()
            if tag:
                response = success_response()
                if action == "view":
                    response['id'] = tag.id
                    response['tag_string'] = tag.tag_string
                    response["message"] = "successfull"
                elif action == "update":
                    tag_string = data.get("tag_string")
                    if tag_string:
                        tag.tag_string = tag_string
                        tag.save()
                    else:
                        response = no_success_response()
                        response["message"] = "Not valid tag string provided for updating the tag"
                else:
                    response = no_success_response()
                    response["message"] = "Not valid action given"
            else:
                response = no_success_response()
                response['message'] = "Not Valid Tag Found"
        else:
            response = no_success_response()
            response['message'] = "Login into the account to view Tag List"
        response['action'] = action
        response['token'] = token
        response['id'] = id
        return response

    class Meta:
        model = Tags
        fields = (
            'id',
            'token',
            'message',
            'status',
            'action',
            'tag_string')


# delete the tag using id
class TagDeleteSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    results = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        id = data.get("id", None)
        status, user = authenticateUser(token)
        if status:
            tag = Tags.objects.filter(id=id, created_by=user).first()
            if tag:
                tag.delete()
                response = success_response()
                response['message'] = "Deleted Tag successfully"
            else:
                response = no_success_response()
                response['message'] = "Not Valid Tag Found"
        else:
            response = no_success_response()
            response['message'] = "Login into the account to delete the Tag"
        response['token'] = token
        response['id'] = id
        return response

    class Meta:
        model = Tags
        fields = (
            'id',
            'token',
            'message',
            'status',
            'results')
