"""
URL configuration for webapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pillPopperPro import views

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('dispense', views.dispense, name='dispense'),
    path('pill_box', views.pill_box, name='pill_box'),
    path('new_pill_form/<int:slot_id>/', views.new_pill_form, name='new_pill_form'),
    path('account',views.login_action, name='account'),
    path('accounts/login/', views.login_action, name='login'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('pillPopperPro/get-pills', views.get_pills),
    path('pill_information/<int:pill_slot>/', views.pill_information, name='pill_information'),
]
