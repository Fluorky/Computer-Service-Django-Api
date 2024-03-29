# Computer-Service-Django
Project of Computer Service web rest API application in Django.

This project is developed rest api version of my other project https://github.com/Fluorky/Computer-Service-Django
The project is part of object-oriented design classes and the project is under development using plantuml diagrams.

# To run this app:
1. git clone https://github.com/Fluorky/Computer-Service-Django-Api.git
2. Go to Computer-Service-Django-Api folder
3. Create and run virtual venv using these commands in cmd 

***Windows***

**py -3 -m venv venv**

**.\\venv\\Scripts\\activate**

***macOS or Linux***

**python3 -m venv venv**

**source ./venv/bin/activate**

4.  Use this command to install requirements packages:

**pip install -r requirements.txt**

5. Use this command to create migrations

**python manage.py makemigrations computerserviceapp**

6. Use this command to create sqlite database from model

**python manage.py migrate**

7. To run app write in cmd

**python manage.py runserver 0.0.0.0:8000**

8. Create superuser 

**python manage.py createsuperuser**

9. Get token and use this token in app, or you must use admin dashboard to create user to get token of these user
Use this address yourIPAddress:8000 with url patch for example:

**http://127.0.0.1:8000/api/token/**

To use this token you should write in http request header

"Authorization" : "Token ***YourToken***"

10. Use this address yourIPAddress:8000 with url patch to integrate with API,for example: ***http://127.0.0.1:8000/api/service-requests/4/***
If you want to check it before, you should use postman or browser.


11. To run unit tests please use this command:

**python manage.py test computerserviceapp**

# Alternate you can use docker

1. Build a Docker image:
In the terminal, while in the project directory, run this command to build a Docker image:

docker-compose build

2. Start the application:
In the terminal, while in the project directory, run this command to run a Docker image:

docker-compose up