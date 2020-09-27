# socialhost

Framework: Django Rest Framework
Database: PostgreSQL 

Steps to be followed:

1. Download the files from github
2. Make database in PostgreSQL with the name of socialhost
3. run python manage.py makemigrations
4. run python manage.py migrate
5. run python manage.py runserver


Test Case 1:
1. Register the user at localhost/api/register/ 
2. Login user at localhost/api/login/
3. Logout user using token at localhost/api/logout/
4. Create tag at localhost/api/tag_create/
5. View tag list at localhost/api/tags_list/
6. View and update single tag at localhost/api/tag_detail/
7. Delete tag at localhost/api/tag_delete/
8. Create post at localhost/api/post_create/
9. View post list at localhost/api/posts_list/
10. View and update single post at localhost/api/post_detail/
11. Delete post at localhost/api/post_delete/


Test case example:
1. Enter username,email,password,name,gender,age,profile_pic as a registration field at register api.
2. Using username or email and password login into the socialhost using login api. The token will generate and copy that token for authentication
3. Logout from socialhost using token at logout api.
4. Create the tag using tag_create api and also add authenticated token.
5. View the tag list using token at tags_list api.

Note:- 1. Use token authentication for all the processes.
	 2. Copy the token while login.

