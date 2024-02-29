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

9. Get token and use this token in app or using admin dashboard create users to using app and get token of these user
Use this address yourIPAddress:8000 with url patch for example:

**http://127.0.0.1:8000/api/token/**

To use this token you should write in http request header

"Authorization" : "Token ***YourToken***"

10. Use this address yourIPAddress:8000 with url patch to integrate with API,for example: ***http://127.0.0.1:8000/api/service-requests/4/***
If you want to check it before, you should use postman or browser.


11. To run unit tests please use this command:

**python manage.py test computerserviceapp**

# Alternate you can use docker

Build a Docker image:
In the terminal, while in the project directory, run the docker build command to build a Docker image:

**docker build -t image_name .**

Where image_name is the name you want to give to your image.

13 Start the container with the image:
Once you've built the image, you can run the container based on it using the command 

**docker run -p 8000:8000 image_name**