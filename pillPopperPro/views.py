from django.shortcuts import render

  
def home_page(request):

    return render(request, 'home.html', {})

def dispense(request):

    return render(request, 'dispense.html', {})

def pill_box(request):

    return render(request, 'pillBox.html', {})

def new_pill_form(request):
   
    return render(request, 'newPillForm.html', {})

def account(request):
    return render(request, 'account.html', {})