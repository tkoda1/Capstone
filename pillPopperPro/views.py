from django.shortcuts import render
from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials
import pytz
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
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json

from django.shortcuts import redirect
from social_django.utils import load_strategy
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile  

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from configparser import ConfigParser
from pathlib import Path


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
@login_required
def update_taken_times(request):
    print("hi - view was triggered")
    
    if request.method == "POST":
        data = json.loads(request.body)
        slot_id = int(data.get("slot"))
        timestamp = data.get("time")
        print(f"Slot: {slot_id}, Timestamp: {timestamp}")

        try:
            pill = Pill.objects.get(user=request.user, pill_slot=slot_id)
            print(f"Found Pill: {pill}")

            timestamp_dt = datetime.datetime.fromisoformat(timestamp).replace(tzinfo=pytz.UTC)

            pill.taken_times.append(timestamp_dt.isoformat())

            seven_days_ago = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=7)

            pill.taken_times = [
                t for t in pill.taken_times if datetime.datetime.fromisoformat(t).replace(tzinfo=pytz.UTC) >= seven_days_ago
            ]

            pill.save()
            print(f"Updated taken times for Pill Slot {slot_id}: {pill.taken_times}")

            return JsonResponse({"status": "success", "taken_times": pill.taken_times})
        
        except Pill.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Pill not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@login_required
def update_timezone(request):
    if request.method == 'POST':
        new_timezone = request.POST.get('timezone')
        if new_timezone:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.timezone = new_timezone
            user_profile.save()
            
            messages.success(request, "Timezone updated successfully!")
        else:
            messages.error(request, "Please select a valid timezone.")

    return redirect('account')  



@login_required
def google_auth_callback(request):
    strategy = load_strategy(request)
    return redirect('/')
  



SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_calendar_service(request):
    user = request.user
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG = ConfigParser()
    CONFIG.read(BASE_DIR / "config.ini")

    if not user.is_authenticated:
        print("User is not authenticated")
        return None  

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
            return None  

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

    for i in range(1, 7):  
        pill = pill_dict.get(i)
        context[f'pill_name{i}'] = pill.name if pill else "Empty"
        context[f'pill_image{i}'] = pill.image.url if pill and pill.image else "/static/pill.jpeg"

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

    for i in range(1, num_slots + 1):  
        pill = pill_dict.get(i)
        context[f'pill_name{i}'] = pill.name if pill else "Empty"
        if( pill and pill.image):
            print(pill.image.url)
        context[f'pill_image{i}'] = pill.image.url if pill and pill.image else "/static/pill.jpeg"

    return render(request, 'pillBox.html', context)


#@login_required
@login_required
def new_pill_form(request, slot_id):
    context = {'id': slot_id}

    if request.method == 'GET':
        context['form'] = PillForm()
        return render(request, 'newPillForm.html', context)

    form = PillForm(request.POST, request.FILES)
    context['form'] = form

    Pill.objects.filter(user=request.user, pill_slot=slot_id).delete()

    if not form.is_valid():
        return render(request, 'newPillForm.html', context)
    
    uploaded_image = form.cleaned_data.get('image')
    if not uploaded_image:
        uploaded_image = "pill.jpeg" 


    new_pill = Pill.objects.create(
        user=request.user,  
        name=form.cleaned_data['name'],
        dosage=form.cleaned_data['dosage'],
        disposal_times=form.cleaned_data['disposal_times'],
        quantity_initial=form.cleaned_data['quantity_initial'],
        quantity_remaining=form.cleaned_data['quantity_initial'],
        pill_slot=slot_id,
        timezone=form.cleaned_data['timezone'],
        image=uploaded_image
    )
    new_pill.save()

    # Add event to Google Calendar
    service = get_google_calendar_service(request)
    print(pytz.timezone(new_pill.timezone).zone)
    

    if service:
        user_timezone = pytz.timezone(new_pill.timezone)  

        for time in form.cleaned_data['disposal_times']:
            
            naive_event_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(time, "%H:%M").time())

           
            event_time = user_timezone.localize(naive_event_time)

            print(f"Event Time (localized to user timezone): {event_time}")

            
            
            event = {
                'summary': f"Take {new_pill.name}",
                'description': f"Dosage: {new_pill.dosage} mg",
                'start': {'dateTime': event_time.isoformat(), 'timeZone': pytz.timezone(new_pill.timezone).zone},
                'end': {'dateTime': (event_time + datetime.timedelta(minutes=15)).isoformat(), 'timeZone': pytz.timezone(new_pill.timezone).zone},
                'recurrence': ['RRULE:FREQ=DAILY'],
            }

            event = service.events().insert(calendarId='primary', body=event).execute()

    #name = 'pill_name' +  str(context['id'])
    #context[name] = form.cleaned_data['name']

    num_slots = 6  
    context = {}

    pills = Pill.objects.filter(user=request.user)
    pill_dict = {pill.pill_slot: pill for pill in pills}

    for i in range(1, num_slots + 1):  
        pill = pill_dict.get(i)
        context[f'pill_name{i}'] = pill.name if pill else "Empty"
        if( pill and pill.image):
            print(pill.image.url)
        context[f'pill_image{i}'] = pill.image.url if pill and pill.image else "/static/pill.jpeg"

    return render(request, 'pillBox.html', context)

#@login_required

@login_required
def account(request):
    """Renders the account page."""
    return render(request, 'account.html', {})


@login_required
def logout_view(request):
    """Logs out the user and redirects to the login page."""
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
    today = now().date()
    last_7_days = [(today - timedelta(days=i)).strftime("%a %m/%d") for i in range(6, -1, -1)]
    hours = [f"{h}:00" for h in range(24)]  

    
    pills = Pill.objects.filter(user=request.user)
    taken_times = []
    scheduled_times = []
    accuracy_stats = {}

    for pill in pills:
        taken_datetimes = []
        correct_takes = 0
        total_scheduled = 0
        pill_timezone = pytz.timezone(pill.timezone)  
        for taken_time in pill.taken_times:
            dt = datetime.datetime.fromisoformat(taken_time)
            dt2 = datetime.datetime.fromisoformat(taken_time).replace(tzinfo=pytz.utc).astimezone(pill_timezone)
            taken_datetimes.append(dt2)
            

        
            
            dt = dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone) 

            day = dt.strftime("%a %m/%d")
            hour = f"{dt.hour}:00"
            time = dt.strftime("%I:%M %p %Z") 

            taken_times.append({
                "day": day,
                "hour": hour,
                "name": pill.name,
                "slot": pill.pill_slot,
                "time": time  
            })
        
        for day_offset in range(7):  
            scheduled_date = today - timedelta(days=day_offset)
            formatted_day = scheduled_date.strftime("%a %m/%d")
            pill_timezone = pytz.timezone(pill.timezone)

            for disposal_time in pill.disposal_times:
                time_obj = datetime.datetime.strptime(disposal_time, "%H:%M").time()
                dt = datetime.datetime.combine(scheduled_date, time_obj)
                dt = dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone)  

                hour = f"{dt.hour}:00"
                time = dt.strftime("%I:%M %p %Z")
                total_scheduled += 1  


                on_time = any(abs((dt - taken_dt).total_seconds()) <= 1800 for taken_dt in taken_datetimes)

                if on_time:
                    correct_takes += 1  

                if not any(t["day"] == formatted_day and t["hour"] == hour and t["name"] == pill.name for t in taken_times):
                    scheduled_times.append({
                        "day": formatted_day,
                        "hour": hour,
                        "name": pill.name,
                        "slot": pill.pill_slot,
                        "time": time,
                    })
        accuracy = round((correct_takes / total_scheduled) * 100, 2) if total_scheduled > 0 else 0
        accuracy_stats[pill.name] = accuracy

    context = {
        "last_7_days": last_7_days,
        "hours": hours,
        "taken_times_json": json.dumps(taken_times),
        "scheduled_times_json": json.dumps(scheduled_times),
        "accuracy_stats": accuracy_stats 
    }

    return render(request, "pillDashboard.html", context)


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
