from django.db import models


class UserProfileInfo(models.Model):
    username = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    age = models.CharField(max_length=3, blank=True)
    profile_image = models.ImageField(max_length=100, blank=True, upload_to='profile_image/')
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return str(self.username)

    def setPersonalInfo(self, name, gender, age, profile_image):
        self.name = name
        self.gender = gender
        self.age = age
        self.profile_image = profile_image

    def createUserProfile(self, username, email, password, name, gender, age, profile_image, ifLogged, token):
        self.username = username
        self.email = email
        self.password = password
        self.ifLogged = ifLogged
        self.token = token
        self.setPersonalInfo(name, gender, age, profile_image)
        self.save()


class Tags(models.Model):
    created_by = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, null=True)
    tag_string = models.CharField(max_length=30, blank=True, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def create(self, tag_string, user):
        self.tag_string = tag_string
        self.created_by = user
        self.save()

    def embed(self):
        return {
            'tag_id':self.id,
            'tag_string':self.tag_string,
            'updated_on':self.updated_on.strftime("%d-%b-%Y (%H:%M:%S)")
        }


class Posts(models.Model):
    created_by = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, null=True)
    post_message = models.CharField(max_length=100, blank=True)
    post_image = models.ImageField(max_length=100, blank=True, upload_to='post_image/')
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def create(self, post_message, post_image, user):
        self.post_message = post_message
        self.post_image = post_image
        self.created_by = user
        self.save()
    
    def embed(self):
        tags_m = TagManager.objects.filter(post_id=self)
        tags = []
        for tag in tags_m:
            tags.append(tag.tag_id.tag_string)

        return {
            'post_id':self.id,
            'post_message':self.post_message,
            'post_image':self.post_image.url if self.post_image else "",
            'post_tags':tags,
            'updated_on':self.updated_on.strftime("%d-%b-%Y (%H:%M:%S)"),
            'created_by':self.created_by.username
        }


class TagManager(models.Model):
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def create(self, tag, post):
        self.tag_id = tag
        self.post_id = post
        self.save()
