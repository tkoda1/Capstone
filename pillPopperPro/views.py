from django.shortcuts import render
from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from pillPopperPro.forms import LoginForm, RegisterForm

from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import PillForm
from .models import Pill
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
import datetime

import json

from django.shortcuts import redirect
from social_django.utils import load_strategy
from google.oauth2.credentials import Credentials


@login_required
def google_auth_callback(request):
    strategy = load_strategy(request)
    return redirect('/')
  



import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from configparser import ConfigParser
from pathlib import Path


SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_calendar_service(request):
    user = request.user
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG = ConfigParser()
    CONFIG.read(BASE_DIR / "config.ini")

    if not user.is_authenticated:
        print("User is not authenticated")
        return None  # User not logged in

    social_auth = user.social_auth.filter(provider='google-oauth2').first()
    if not social_auth:
        print("No social_aut object found for user")
        return None

    extra_data = social_auth.extra_data
    access_token = extra_data.get('access_token')
    refresh_token = extra_data.get('refresh_token')

    print(f"social Auth Data: {extra_data}")

    if not access_token:
        print("No access token found")
        return None

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CONFIG.get("GoogleOAuth2", "client_id"),
        client_secret=CONFIG.get("GoogleOAuth2", "client_secret"),
        scopes=SCOPES,
    )
    if not creds.valid:
        try:
            print("Refreshing expired token...")
            creds.refresh(Request())
            print("Token refreshed successfully!")
        except Exception as e:
            print(f"Error refreshing token: {e}")
            print("User must re-authenticate.")
            return None  # Token refresh failed, user must log in again

    print(f"Credentials Object: {creds}")
    print(f"User's granted scopes: {creds.scopes}")

    if not creds.scopes or 'https://www.googleapis.com/auth/calendar.events' not in creds.scopes:
        print("Missing required Google Calendar scopes. User must log in again.")
        return None  # Missing scopes

    return build("calendar", "v3", credentials=creds)

  

@login_required
def home_page(request):
    return render(request, 'home.html', {})


@login_required
def dispense(request):
    context = {}
    pills = Pill.objects.filter(user=request.user)
    pill_dict = {pill.pill_slot: pill for pill in pills}

    slots = []
    for i in range(7):
        if i in pill_dict:
            slots.append(pill_dict.get(i, None))
            name = 'pill_name' + str(i)
            context[name] = 'slot ' + str(i) + ': ' + pill_dict[i].name
        else:
            name = 'pill_name' + str(i)
            context[name] = 'slot ' + str(i) + ': empty'

    return render(request, 'dispense.html', context)


#@login_required
@login_required
def pill_information(request, pill_slot):
    pill = Pill.objects.filter(user=request.user, pill_slot=pill_slot).first()  

    context = {
        'pill': pill
    }
    return render(request, 'PillInformation.html', context)



#@login_required
@login_required
def pill_box(request):
    num_slots = 6  
    context = {}
    pills = Pill.objects.filter(user=request.user)
    pill_dict = {pill.pill_slot: pill for pill in pills}

    slots = []
    #ranges though the 6 diffrent pill slots rendering names 
    for i in pill_dict:
        slots.append(pill_dict.get(i, None))  
        name = 'pill_name' +  str(i)
        context[name] = pill_dict[i].name



    return render(request, 'pillBox.html', context)

#@login_required
@login_required
def new_pill_form(request, slot_id):
    context = {'id': slot_id}

    if request.method == 'GET':
        context['form'] = PillForm()
        return render(request, 'newPillForm.html', context)

    form = PillForm(request.POST)
    context['form'] = form

    # Ensure pills are deleted only for the current user in the given slot
    Pill.objects.filter(user=request.user, pill_slot=slot_id).delete()

    if not form.is_valid():
        return render(request, 'newPillForm.html', context)

    # 🔹 Save pill **with user association**
    new_pill = Pill.objects.create(
        user=request.user,  # 🔹 Store the user
        name=form.cleaned_data['name'],
        dosage=form.cleaned_data['dosage'],
        disposal_times=form.cleaned_data['disposal_times'],
        quantity_initial=form.cleaned_data['quantity_initial'],
        quantity_remaining=form.cleaned_data['quantity_initial'],
        pill_slot=slot_id,
    )
    new_pill.save()

    # Add event to Google Calendar
    service = get_google_calendar_service(request)

    if service:
        for time in form.cleaned_data['disposal_times']:
            # Convert time to proper datetime
            event_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(time, "%H:%M").time())

            event = {
                'summary': f"Take {new_pill.name}",
                'description': f"Dosage: {new_pill.dosage} mg",
                'start': {'dateTime': event_time.isoformat(), 'timeZone': 'UTC'},
                'end': {'dateTime': (event_time + datetime.timedelta(minutes=30)).isoformat(), 'timeZone': 'UTC'},
                'recurrence': ['RRULE:FREQ=DAILY'],
            }

            event = service.events().insert(calendarId='primary', body=event).execute()

    name = 'pill_name' +  str(context['id'])
    context[name] = form.cleaned_data['name']

    pills = Pill.objects.filter(user=request.user)
    pill_dict = {pill.pill_slot: pill for pill in pills}

    for i in pill_dict:
        name = 'pill_name' + str(i)
        context[name] = pill_dict[i].name

    return render(request, 'pillBox.html', context)

#@login_required

@login_required
def account(request):
    """Renders the account page."""
    return render(request, 'account.html', {})


@login_required
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    # Regular logout for non-OAuth users
    logout(request)
    return redirect("login")


def login_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

  
    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        context['error'] = forms.ValidationError("Invalid username/password")
        return render(request, 'login.html', context)


    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    if new_user is not None:
        login(request, new_user)
        first_name = new_user.first_name
        context['globalField'] = forms.CharField(max_length=20)
        user_name1 = User.objects.get(username=form.cleaned_data['username'])
        #context['name_of_user'] = 
        context['name_of_user'] = new_user.first_name + " " + new_user.last_name 
    
        return render(request, 'home.html', context)
    else:
        context['error'] = forms.ValidationError("Invalid username/password")
        return render(request, 'login.html', context)
    

def register_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

  
    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    context['name_of_user'] = form.cleaned_data['first_name'] +" " +form.cleaned_data['last_name']

    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    return render(request, 'pillDashboard.html', {})

@login_required
def get_pills(request):
    pills = []
    for p in Pill.objects.all().order_by('pill_slot'):
        pill = {
            'name': p.name,
            'dosage': p.dosage,
            'disposal_times': p.disposal_times,
            'quantity_initial': p.quantity_initial,
            'quantity_remaining': p.quantity_remaining,
            'pill_slot': p.pill_slot,
            'taken_today': p.taken_today
        }
        pills.append(pill)
    response_data = {'pills': pills}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')



@login_required
def check_authentication(request):
    return JsonResponse({"user": request.user.username, "is_authenticated": request.user.is_authenticated})
