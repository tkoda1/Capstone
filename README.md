# Capstone
Shared capstone project for PillPopperPro

Setting up your environment: 
```
   python3 -m venv venv .
   <activate the virtual environment>
   python -m pip install -U pip
   python -m pip install -r requirements.txt
```

Then run the demo in the usual way:
```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
```
*Oath*
If attempting to try Oath logging please use school email as other emails are not authorized. Additionally if secret key is needed contact Taylor.


*Celery locally*
One terminal: python manage.py runserver
Another terminal: celery -A webapps worker --loglevel=info
Yet another terminal: celery -A webapps beat --loglevel=info


References & Sources:
17437 homework 7

17437 fall 24 team 19 project

17437 fall 23 team 19 project

17437 lecture 13 jQuery & WebSockets

17437 websockets coding example

17437 Fall 2023 Lecture 17 Passwords & Oath

17437 Fall 2023 Lecture 4 HTTP & Django

https://www.w3schools.com/js/js_date_methods.asp

https://www.freecodecamp.org/news/how-to-convert-a-string-to-a-number-in-javascript/

https://www.w3schools.com/jsref/jsref_substring.asp

https://www.w3schools.com/jsref/met_win_confirm.asp

https://www.geeksforgeeks.org/passing-a-function-as-a-parameter-in-javascript/

https://developers.google.com/identity/sign-in/web/sign-in 

https://chatgpt.com/share/67fd6fd5-d66c-8000-9abd-c118a1fe5dcb

https://chatgpt.com/share/67fef1e4-8cc8-8000-b385-658fbb5e7078

https://chatgpt.com/share/67fef1f0-131c-8000-8e97-3b8d6d075d41

https://chatgpt.com/share/67fef1fd-7f04-8000-a4e1-dd1d61eafb59

https://chatgpt.com/share/67fef214-ce00-8000-9989-a21ddee4b8cc

https://chatgpt.com/share/67ffc83b-921c-8000-a1e7-ab0baddda841

https://chatgpt.com/share/67ffce38-9dc0-8000-a0b8-61a6333579a3

https://chatgpt.com/share/68017db6-67ec-8000-8387-6703e2a43a70

https://chatgpt.com/share/68067f03-8dd0-8000-8b6d-2d6bd97b5eca

https://docs.python.org/3/library/textwrap.html

https://chatgpt.com/share/6806f1b4-edf0-8000-8e02-cc89a067a968