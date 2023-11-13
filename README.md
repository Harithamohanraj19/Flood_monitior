# Flood_monitor
Real-time flood monitoring using Django and external environmental APIs.

Introduction

This project is a web application developed in Python using the Django framework. It utilizes real-time flood monitoring data from external environmental APIs to provide users with information about water levels and stages at various monitoring stations.

Prerequisites

    python >= v3.6.9
    django >= v3.2
    Ubuntu 18.04.6 LTS


Setup
   
   1. The first thing to do is to clone the repository
        $ git clone https://github.com/Harithamohanraj19/flood_monitor.git
        $ cd Flood_monitior

   2. Create a virtual environment to install dependencies in and activate it
        
    (env)$ pip3 install django

    (env)$ pip3 install requests

    (env)$ pip3 install matplotlib tabulate


How to run the script
    
    Web Application

        (env)$ python manage.py runserver  

        And navigate to http://127.0.0.1:8000/

    Script
        (env)$ python3 script.py

Tests

    (env)$ python manage.py test your_app.tests.test_views

Tested on enviornment
    
    Ubuntu 18.04.6 LTS
    python  v3.6.9
    django  v3.2
