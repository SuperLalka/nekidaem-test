# nekidaem-test
Test project of a blog site in Django, with user authentication and authorization. 

For authorization 
-----------------
JWT is used which is available with the indication of the username and password at:
- token/
# Requirements
The project was built in Django using the following requirements:
- tinymce,
- drf_yasg
# Deploy
The project is mounted on docker, to deploy it you need:

Create an image
> docker build .

Collect the image with the command:
> docker-compose -f docker-compose.yml up -d --build

To connect to the site use the nginx port (default: 1337)

To the project added a swagger available at
-------------------------------------------
- swagger/