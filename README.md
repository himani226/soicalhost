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


