from rest_framework import serializers
from socialgram.models import UserProfileInfo, Tags, Posts, TagManager
from socialgram.utility import authenticateUser, success_response, no_success_response, INVALID_SESSION_RESPONSE


# create the post using serializers
class PostCreateSerializer(serializers.ModelSerializer):
    post_message = serializers.CharField(required=True)
    post_image = serializers.ImageField(required=False)
    post_tag = serializers.CharField(required=False)
    token = serializers.CharField(required=True)
    status = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)
    post_message = serializers.CharField(required=True)
    post_image = serializers.ImageField(required=False)
    post_tag = serializers.CharField(required=False)

    def validate(self, data):
        token = data.get("token")
        post_message = data.get("post_message", None)
        post_image = data.get("post_image", None)
        post_tag = data.get("post_tag", None)
        # validate the user detail
        status, user = authenticateUser(token)
        if status:
            valid_tags = True
            valid_tags_obj = []
            if post_tag:
                for tag in post_tag.split(","):
                    tag = Tags.objects.filter(tag_string=tag, created_by=user).first()
                    if not tag:
                        valid_tags = False
                        break
                    else:
                        valid_tags_obj.append(tag)

                if not valid_tags:
                    # implies not valid tag has been used and break the loop and reject the post creating
                    response = no_success_response()
                    response['message'] = "Not valid tag has been used"
                    response['token'] = token
                    response['post_tag'] = post_tag
                    response['post_message'] = post_tag
                    response['post_image'] = post_image
                    return response

            post = Posts()
            post.create(post_message, post_image, user)
            for tag in valid_tags_obj:
                tag_m = TagManager()
                tag_m.create(tag, post)
            response = success_response()
        else:
            response = user

        response['post_tag'] = post_tag
        response['post_message'] = post_message
        response['post_image'] = post_image
        response['token'] = token
        return response

    class Meta:
        model = Posts
        fields = ("status",
                  "message",
                  "token",
                  "post_message",
                  "post_image",
                  "post_tag")


class PostListViewSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    results = serializers.JSONField(required=False, read_only=True)
    tags = serializers.CharField(required=False)

    def validate(self, data):
        posts = []
        tags = data.get("tags")
        tags_mg = []
        if tags:
            tags = tags.split(",")
            tags_obj = Tags.objects.filter(tag_string__in=tags)
            tags_mg = TagManager.objects.filter(tag_id__in=tags_obj)
        if tags_mg:
            posts_ids = [p.post_id.id for p in tags_mg]
            posts_obj = Posts.objects.filter(id__in=posts_ids)
        else:
            posts_obj = Posts.objects.all()
        for p in posts_obj:
            posts.append(p.embed())
        response = success_response()
        response['results'] = posts
        return response

    class Meta:
        model = Posts
        fields = (
            'results',
            'message',
            'status',
            "tags")


#get the list of posts and update it using update action
class PostGetViewSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)
    action = serializers.CharField(required=False)
    message = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)
    post_message = serializers.CharField(required=False)
    post_tags = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        id = data.get("id", None)
        action = data.get("action", "view")
        status, user = authenticateUser(token)
        if status:
            post = Posts.objects.filter(id=id, created_by=user).first()
            if post:
                if action == "view":
                    response = success_response()
                    response['post_message'] = post.post_message
                    tag_m = TagManager.objects.filter(post_id=post)
                    tags = [tag.tag_id.tag_string for tag in tag_m]
                    response['post_tags'] = ",".join(tags)
                elif action == "update":
                    response = success_response()
                    post_message = data.get("post_message")
                    if post_message:
                        post.post_message = post_message
                        post.save()
                    else:
                        response = no_success_response()
                        response["message"] = "Not valid post message given"
                else:
                    response = no_success_response()
                    response["message"] = "Not valid action given"
            else:
                response = no_success_response()
                response['message'] = "Not valid post found"
        else:
            response = no_success_response()
            response['message'] = "Login into the account to view user Post"
        response['action'] = action
        response['token'] = token
        response['id'] = id
        return response

    class Meta:
        model = Posts
        fields = (
            'id',
            'token',
            'action',
            'message',
            'status',
            'post_message',
            'post_tags')

#delete the post by providing id
class PostDeleteViewSerializer(serializers.ModelSerializer):
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
            post = Posts.objects.filter(id=id, created_by=user).first()
            if post:
                post.delete()
                response = success_response()
                response['message'] = "Deleted Post successfully"
            else:
                response = no_success_response()
                response['message'] = "Not Valid Post Found"
        else:
            response = no_success_response()
            response['message'] = "Login into the account to delete Post"
        response['token'] = token
        response['id'] = id
        return response

    class Meta:
        model = Posts
        fields = (
            'id',
            'token',
            'message',
            'status',
            'results')
