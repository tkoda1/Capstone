from django.shortcuts import render
from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
import json
  

#@login_required
def home_page(request):

    return render(request, 'home.html', {})

#@login_required
def dispense(request):
    context = {}
    pills = Pill.objects.all()
    pill_dict = {pill.pill_slot: pill for pill in pills}  

    slots = []
    #ranges though the 6 diffrent pill slots rendering names 
    for i in range (7):
        if i in pill_dict:
            slots.append(pill_dict.get(i, None))  
            name = 'pill_name' +  str(i)
            context[name] = 'slot ' + str(i) + ': ' +  pill_dict[i].name
        else:
            name = 'pill_name' +  str(i)
            context[name] = 'slot ' + str(i) + ': empty'


    return render(request, 'dispense.html', context)

#@login_required
def pill_box(request):
    num_slots = 6  
    context = {}
    pills = Pill.objects.all()
    pill_dict = {pill.pill_slot: pill for pill in pills}

    slots = []
    #ranges though the 6 diffrent pill slots rendering names 
    for i in pill_dict:
        slots.append(pill_dict.get(i, None))  
        name = 'pill_name' +  str(i)
        context[name] = pill_dict[i].name



    return render(request, 'pillBox.html', context)

#@login_required
def new_pill_form(request, slot_id):
    context = {}
    context['id'] = slot_id


    if request.method == 'GET':
        context['form'] = PillForm()
        return render(request, 'newPillForm.html', context)

    form = PillForm(request.POST)
    context['form'] = form
    context['id'] = slot_id
    Pill.objects.filter(pill_slot=slot_id).delete()


    if not form.is_valid():
        return render(request, 'newPillForm.html', context)


    # Saving new pills id number important for logic
    new_pill = Pill.objects.create(
        name=form.cleaned_data['name'],
        dosage=form.cleaned_data['dosage'],
        disposal_times=form.cleaned_data['disposal_times'],
        quantity_initial=form.cleaned_data['quantity_initial'],
        quantity_remaining=form.cleaned_data['quantity_initial'],
        pill_slot = context['id']
    )
    new_pill.save()
    name = 'pill_name' +  str(context['id'])
    context[name] = form.cleaned_data['name']

    pills = Pill.objects.all()
    pill_dict = {pill.pill_slot: pill for pill in pills} 

    slots = []
    #i dont think this may be needed repeat logic but its for pillbox rendering
    for i in pill_dict:
        slots.append(pill_dict.get(i, None))  
        name = 'pill_name' +  str(i)
        context[name] = pill_dict[i]


    return render(request, 'pillBox.html', context)  # Redirect to a success page

#@login_required
def account(request):
    return render(request, 'account.html', {})

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

def dashboard(request):
    return render(request, 'pillDashboard.html', {})

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