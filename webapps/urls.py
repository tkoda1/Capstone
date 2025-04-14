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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



urlpatterns = [
    path('', views.home_page, name='root'), 
    path('oauth/', include('social_django.urls', namespace='social')),
    #path('dispense', views.dispense, name='dispense'),
    path('dispense/', views.dispense, name='dispense'),
    path('pill_box', views.pill_box, name='pill_box'),
    path('new_pill_form/<int:slot_id>/', views.new_pill_form, name='new_pill_form'),
    path('account',views.account, name='account'),
    path('accounts/login/', views.login_action, name='login'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('pillPopperPro/get-pills', views.get_pills),
    path('logout/', views.logout_view, name='logout'),
    path('pill_information/<int:pill_slot>/', views.pill_information, name='pill_information'),
    path("check-auth/", views.check_authentication, name="check_auth"),
    path('oauth2callback/', views.google_auth_callback, name='google_auth_callback'),
    path('update_timezone/', views.update_timezone, name='update_timezone'),
    path("update_taken_times/", views.update_taken_times, name="update_taken_times"),
    path('patient-tracker/', views.patient_tracker, name='patient_tracker'),
    path('patient-dashboard/<str:username>/', views.patient_dashboard, name='patient_dashboard'),
    path('add-caretaker/', views.add_caretaker, name='add_caretaker'),
    path('account-caretaker', views.account_caretaker, name='account_caretaker'),
    path('remove-caretaker/', views.remove_caretaker, name='remove_caretaker'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
