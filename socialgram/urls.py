from django.urls import path
from socialgram.login.views import Register, Login, Logout
from socialgram.tags.views import Tag_create, Tag_list, Tag_delete, Tag_detail
from socialgram.post.views import Post_create, Post_list, Post_detail, Post_delete

urlpatterns = [
    path('register/', Register.as_view(), name="register"), #registration url
    path('login/', Login.as_view(), name="login"), #login url
    path('logout/', Logout.as_view(), name="logout"), #logout url
    path('tag_create/', Tag_create.as_view(), name="tags"), #create tags
    path('tags_list/', Tag_list.as_view(), name="tag_list"), #view all the tags list
    path('tag_detail/', Tag_detail.as_view(), name="tag_detail"),#view and update the single tag
    path('tag_delete/', Tag_delete.as_view(), name="tag_delete"), #delete the single tag
    path('post_create/', Post_create.as_view(), name="post"), #create post
    path('posts_list/', Post_list.as_view(), name="post_list"), #view all the post list
    path('post_detail/',Post_detail.as_view(), name= "post_detail"), # view and update detail of single post
    path('post_delete/',Post_delete.as_view(), name= "post_delete") #delete the single post
]