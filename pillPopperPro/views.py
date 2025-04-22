import datetime
import json
import os
from configparser import ConfigParser
from pathlib import Path

import pytz
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pillPopperPro.forms import LoginForm, RegisterForm
from social_django.utils import load_strategy
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import PillForm
from .models import Pill, UserProfile


# Every time the dispense button is clicked the time is calculated and added to a list
#corresponding with the pill. It is then rendered on the dashboard as the times the pills where taken
#each medication is rendereed in a diffrent color
#TODO: make sure the times are right 
@csrf_exempt
@login_required
def update_taken_times(request):
    print('VIEWS.PY UPDATE TAKE TIMES FUNCTION')
    # print("hi - view was triggered")
    if request.method == "POST":
        print('VIEWS.PY UPDATE TAKE TIMES POST FUNCTION')
        data = json.loads(request.body)
        slot_id = int(data.get("slot"))
        timestamp = data.get("time")
        # print(f"Slot: {slot_id}, Timestamp: {timestamp}")

        try:
            pill = Pill.objects.get(user=request.user, pill_slot=slot_id)
            # print(f"Found Pill: {pill}")

            timestamp_dt = datetime.datetime.fromisoformat(timestamp).replace(tzinfo=pytz.UTC)
            pill.taken_times.append(timestamp_dt.isoformat())
            seven_days_ago = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=7)

            pill.taken_times = [
                t for t in pill.taken_times if datetime.datetime.fromisoformat(t).replace(tzinfo=pytz.UTC) >= seven_days_ago
            ]

            pill.save()
            # print(f"Updated times for Pill Slot {slot_id}: {pill.taken_times}")

            return JsonResponse({"status": "success", "taken_times": pill.taken_times})
        
        except Pill.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Pill not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


#TODO:DELete I do notlike this it is for the acccount page though it may be needed
#it associates a time zone with the user and lets them change it 
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



#Tring to get the OAth to work 
@login_required
def google_auth_callback(request):
    strategy = load_strategy(request)
    return redirect('/')
  


SCOPES = ['https://www.googleapis.com/auth/calendar.events']


#This is just needed in order to be able to use the google calander API and add events
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
        return None  

    return build("calendar", "v3", credentials=creds)

  

#Renders home page
@login_required
def home_page(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    #return render(request, 'account.html', {
    #    'user_profile': user_profile,
    #    'caretakers': caretakers
    #})
    context = {}
    context['user_profile'] = user_profile

    if user_profile.role == 'caretaker':
        return redirect('patient_tracker')
    else:
        return render(request, 'home.html', context)



#This is the functionalitu for the dispense page
#has both post and get post is so that the like pill quantity goes down
#get is just to render the general dispensal page. The logic is a little weird
@login_required
def dispense(request):
    print('VIEWS.PY DISPENSE FUNCTION')
    if request.method == "POST":
        print('VIEWS.PY DISPENSE POST FUNCTION')
        # print("heyyyy")
        data = json.loads(request.body)
        pill_slot = data.get("slot")

        try:
            pill = Pill.objects.get(user=request.user, pill_slot=pill_slot)
            print(pill.quantity_remaining)
            print(pill.slot_angle)

            # check to make sure the user isn't taking more than the dosage
            if pill.taken_today >= pill.dosage:
                return JsonResponse({"success": False, "error": 
                    "Cannot dispense more pills than the specified dosage"}, 
                    status=200)

            #weirdly always one off also need to add new notifcation about when empty 
            if pill.quantity_remaining > 0:
                slot_angle = pill.slot_angle
                pill.quantity_remaining -= 1
                pill.taken_today = 1
                if slot_angle == 0:
                    print('Updating angle from 0 to 180')
                    pill.slot_angle = 180
                else:
                    print('Updating angle from 180 to 0')
                    pill.slot_angle = 0
                # print(pill)
                pill.save()
                #print(type(pill.quantity_remaining))
                print(pill.quantity_remaining)
                print(pill.slot_angle)
                print(pill)

 
                refill_warning = pill.quantity_remaining <= 3
                # print(pill.quantity_remaining)

                return JsonResponse({
                    "success": True,
                    "quantity_remaining": pill.quantity_remaining,
                    "refill_warning": refill_warning,
                    "pill_slot": pill_slot,
                    "slot_angle": slot_angle
                })
                
            else:
                return JsonResponse({"success": False, "error": "This compartment is empty, please refill with more pills", "no_pills": True}, status=400)

        except Pill.DoesNotExist:
            return JsonResponse({"success": False, "error": "Pill not found"}, status=404)

    # old
    context = {}
    pills = Pill.objects.filter(user=request.user)
    pill_dict = {pill.pill_slot: pill for pill in pills}

    for i in range(1, 7):  
        pill = pill_dict.get(i)
        context[f'pill_name{i}'] = pill.name if pill else "Empty"
        context[f'pill_image{i}'] = pill.image.url if pill and pill.image else "/static/pill.jpeg"

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

    return render(request, 'dispense.html', context)


#@login_required
@login_required
def pill_information(request, pill_slot):
    pill = Pill.objects.filter(user=request.user, pill_slot=pill_slot).first()  

    context = {
        'pill': pill
    }

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile
    return render(request, 'PillInformation.html', context)



#@login_required

#Renderes the pillBox page by cycling though the entered pills if a pill was not entered
#a defult value is just put in 
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

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

    return render(request, 'pillBox.html', context)


#Mess with this and we willl have words
#THis is the form where users enter in information about their medication 
#users can enter in multiple times to take a medicaiton
#@login_required
@login_required
def new_pill_form(request, slot_id):
    context = {'id': slot_id}
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)


    context['user_profile'] = user_profile

    #modified this so that previous pill informaiton is rendered 
    if request.method == 'GET':
        try:
            existing_pill = Pill.objects.get(user=request.user, pill_slot=slot_id)
            initial_data = {
                'name': existing_pill.name,
                'dosage': existing_pill.dosage,
                'quantity_initial': existing_pill.quantity_initial,
                'disposal_times': existing_pill.disposal_times,
                'timezone': existing_pill.timezone,
                'days_of_week': existing_pill.days_of_week,
                'image': existing_pill.image
            }

            context['form'] = PillForm(initial=initial_data)
            context['selected_disposal_times'] = existing_pill.disposal_times
        except Pill.DoesNotExist:
            context['form'] = PillForm()

        return render(request, 'newPillForm.html', context)


    form = PillForm(request.POST, request.FILES)
    context['form'] = form
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

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
        days_of_week=form.cleaned_data['days_of_week'],
        quantity_initial=form.cleaned_data['quantity_initial'],
        quantity_remaining=form.cleaned_data['quantity_initial'],
        pill_slot=slot_id,
        timezone=form.cleaned_data['timezone'],
        image=uploaded_image
    )

    new_pill.save()

    
    service = get_google_calendar_service(request)
    print(pytz.timezone(new_pill.timezone).zone)
    

    #if the user is logged in via gCAL then the notfication is added to the calander
    if service:
        user_timezone = pytz.timezone(new_pill.timezone)  

        for time in form.cleaned_data['disposal_times']:
            #make sure on day
            naive_event_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(time, "%H:%M").time())
            event_time = user_timezone.localize(naive_event_time)

            event = {
                'summary': f"Take {new_pill.name}",
                'description': f"Dosage: {new_pill.dosage} mg",
                'start': {'dateTime': event_time.isoformat(), 'timeZone': new_pill.timezone},
                'end': {'dateTime': (event_time + datetime.timedelta(minutes=15)).isoformat(), 'timeZone': new_pill.timezone},
                'recurrence': [f'RRULE:FREQ=WEEKLY;BYDAY={",".join(form.cleaned_data["days_of_week"])}']
            }

            service.events().insert(calendarId='primary', body=event).execute()


    #name = 'pill_name' +  str(context['id'])
    #context[name] = form.cleaned_data['name']

    #needed to render the pill box page. Could this have been done better? yes
    num_slots = 6  
    context = {}
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

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
def add_caretaker(request):
    if request.method == 'POST':
        username = request.POST.get('caretaker_username')
        try:
            caretaker = User.objects.get(username=username)
            caretaker_profile = UserProfile.objects.get(user=caretaker)

            if caretaker_profile.role != 'caretaker':
                messages.error(request, f"{username} is not a registered caretaker.")
            else:
                patient_profile = UserProfile.objects.get(user=request.user)
                patient_profile.caretakers.add(caretaker)
                messages.success(request, f"{username} added as a caretaker.")

        except User.DoesNotExist:
            messages.error(request, f"No user with username: {username}")
        except UserProfile.DoesNotExist:
            messages.error(request, f"{username} does not have a profile.")

    return redirect('account')


@login_required
def account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    caretakers = user_profile.caretakers.all() if user_profile.role == 'patient' else []

    return render(request, 'account.html', {
        'user_profile': user_profile,
        'caretakers': caretakers
    })



@login_required
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect("login")


#from web app


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
        context['name_of_user'] = new_user.first_name + " " + new_user.last_name
        context['globalField'] = forms.CharField(max_length=20)

        try:
            user_profile = UserProfile.objects.get(user=new_user)
            if user_profile.role == 'caretaker':
                return redirect('patient_tracker')
        except UserProfile.DoesNotExist:
            pass  

        return render(request, 'home.html', context)
    else:
        context['error'] = forms.ValidationError("Invalid username/password")
        return render(request, 'login.html', context)

    
#from web app
def register_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)
    
    new_user = User.objects.create_user(
        username=form.cleaned_data['username'], 
        password=form.cleaned_data['password'],
        email=form.cleaned_data['email'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name']
    )


    UserProfile.objects.create(
        user=new_user,
        role=form.cleaned_data['role'],
    )

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)

    role = form.cleaned_data['role']
    if role == 'caretaker':
        return redirect('patient_tracker') 
    else:
        return redirect('root')


@login_required
def dashboard(request):
    today = now().date()
    #gpt used for seven day logic and shifting times
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
            if dt.tzinfo is None:
                dt = pill_timezone.localize(dt)
            dt2 = dt.astimezone(pytz.timezone('US/Eastern'))
            #dt2 = dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone)
            taken_datetimes.append(dt2)

            day = dt2.strftime("%a %m/%d")
            hour = f"{dt2.hour}:00"
            time = dt2.strftime("%I:%M %p %Z")

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
            #from the stored user input
            weekday_code = scheduled_date.strftime("%a").upper()[:2] 

            #skips the day if not seen
            if weekday_code not in pill.days_of_week:
                continue 

            for disposal_time in pill.disposal_times:
                time_obj = datetime.datetime.strptime(disposal_time, "%H:%M").time()
                scheduled_dt = datetime.datetime.combine(scheduled_date, time_obj)
                scheduled_dt = pill_timezone.localize(scheduled_dt)
                #scheduled_dt = datetime.datetime.combine(scheduled_date, time_obj)
                #scheduled_dt = scheduled_dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone)

                hour = f"{scheduled_dt.hour}:00"
                time = scheduled_dt.strftime("%I:%M %p %Z")
                total_scheduled += 1

                on_time = any(abs((scheduled_dt - taken_dt).total_seconds()) <= 1800 for taken_dt in taken_datetimes)
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

        #calculates accuracy rendered at top
        accuracy = round((correct_takes / total_scheduled) * 100, 2) if total_scheduled > 0 else 0
        accuracy_stats[pill.name] = accuracy

    #renders
    context = {
        "last_7_days": last_7_days,
        "hours": hours,
        "taken_times_json": json.dumps(taken_times),
        "scheduled_times_json": json.dumps(scheduled_times),
        "accuracy_stats": accuracy_stats
    }

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

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


@login_required
def patient_tracker(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != 'caretaker':
        return render(request, 'unauthorized.html', {'message': 'Access denied: not a caretaker.'})

    context = {}

    username_query = request.GET.get('username')
    if username_query:
        try:
            patient_user = User.objects.get(username=username_query)
            patient_profile = UserProfile.objects.get(user=patient_user)

            if patient_profile.role != 'patient':
                context['error'] = f"{username_query} is not registered as a patient."
            else:
                context['patient'] = patient_user

        except User.DoesNotExist:
            context['error'] = f"No user found with username: {username_query}"
        except UserProfile.DoesNotExist:
            context['error'] = f"{username_query} does not have a profile set up."

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context['user_profile'] = user_profile

    return render(request, 'patientTracker.html', context)

@login_required
def patient_dashboard(request, username):
    caretaker_profile = UserProfile.objects.get(user=request.user)

    if caretaker_profile.role != 'caretaker':
        messages.error(request, 'Access denied: not a caretaker.')
        return redirect('patient_tracker')

    try:
        patient_user = User.objects.get(username=username)
        patient_profile = UserProfile.objects.get(user=patient_user)

        if caretaker_profile.user not in patient_profile.caretakers.all():
            messages.error(request, f"You are not assigned to view {username}'s dashboard.")
            return redirect('patient_tracker')

        context = get_pill_dashboard_context(patient_user)
        context['patient'] = patient_user
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        context['user_profile'] = user_profile
        return render(request, 'pillDashboard.html', context)

    except User.DoesNotExist:
        messages.error(request, f"No user found with username: {username}")
        return redirect('patient_tracker')



def get_pill_dashboard_context(user):
    today = now().date()
    last_7_days = [(today - datetime.timedelta(days=i)).strftime("%a %m/%d") for i in range(6, -1, -1)]
    hours = [f"{h}:00" for h in range(24)]

    pills = Pill.objects.filter(user=user)
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
            dt2 = dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone)
            taken_datetimes.append(dt2)

            day = dt2.strftime("%a %m/%d")
            hour = f"{dt2.hour}:00"
            time = dt2.strftime("%I:%M %p %Z")

            taken_times.append({
                "day": day,
                "hour": hour,
                "name": pill.name,
                "slot": pill.pill_slot,
                "time": time
            })

        for day_offset in range(7):
            scheduled_date = today - datetime.timedelta(days=day_offset)
            formatted_day = scheduled_date.strftime("%a %m/%d")
            weekday_code = scheduled_date.strftime("%a").upper()[:2] 

            if weekday_code not in pill.days_of_week:
                continue

            for disposal_time in pill.disposal_times:
                time_obj = datetime.datetime.strptime(disposal_time, "%H:%M").time()
                scheduled_dt = datetime.datetime.combine(scheduled_date, time_obj)
                scheduled_dt = scheduled_dt.replace(tzinfo=pytz.utc).astimezone(pill_timezone)

                hour = f"{scheduled_dt.hour}:00"
                time = scheduled_dt.strftime("%I:%M %p %Z")
                total_scheduled += 1

                on_time = any(abs((scheduled_dt - taken_dt).total_seconds()) <= 1800 for taken_dt in taken_datetimes)
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

    return {
        "last_7_days": last_7_days,
        "hours": hours,
        "taken_times_json": json.dumps(taken_times),
        "scheduled_times_json": json.dumps(scheduled_times),
        "accuracy_stats": accuracy_stats
    }

@login_required
def account_caretaker(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != 'caretaker':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('account')

    patients = request.user.patients.all()

    return render(request, 'accountCareTaker.html', {
        'user_profile': user_profile,
        'patients': patients
    })


@login_required
def remove_caretaker(request):
    if request.method == 'POST':
        username = request.POST.get('caretaker_username')
        try:
            caretaker = User.objects.get(username=username)
            caretaker_profile = UserProfile.objects.get(user=caretaker)

            if caretaker_profile.role != 'caretaker':
                messages.error(request, f"{username} is not a registered caretaker.")
            else:
                patient_profile = UserProfile.objects.get(user=request.user)
                patient_profile.caretakers.remove(caretaker)
                messages.success(request, f"{username} has been removed from your caretakers.")
        except User.DoesNotExist:
            messages.error(request, f"No user with username: {username}")
        except UserProfile.DoesNotExist:
            messages.error(request, f"{username} does not have a profile.")

    return redirect('account')

def get_schedule_reminder(request):
    print('Scheduled reminder views.py')
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    user = request.user
    pills = Pill.objects.filter(user=user)
    curr_datetime = datetime.datetime.now()
    pills_to_take = []
    for pill in pills:
        take_time = datetime.datetime.strptime(pill.disposal_times[0], "%H:%M").time()
        take_datetime = datetime.datetime.combine(datetime.date.today(), take_time)
        if (curr_datetime > take_datetime) and (pill.taken_today == 0):
            pills_to_take.append(pill.name)

    return JsonResponse({"status": "success", 'pills': pills_to_take})

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)


def get_refill_reminder(request):
    print('Refill reminder views.py')
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    user = request.user
    pills = Pill.objects.filter(user=user)
    refills = []
    upcoming_refills = []
    refill_threshold = 10
    for pill in pills:
        if pill.quantity_remaining <= 0:
            refills.append(pill.name)
        elif pill.quantity_remaining <= refill_threshold:
            upcoming_refills.append(pill.name)
            print(pill.name)

    return JsonResponse({"status": "success",
                         'upcoming_refills': upcoming_refills,
                        'refills': refills})