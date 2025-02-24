from django.test import TestCase

# Create your tests here.

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context['error'] = forms.ValidationError("Invalid username/password")
        return render(request, 'login.html', context)
    #form = LoginForm(request.POST)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    if new_user is not None:
        login(request, new_user)
        first_name = new_user.first_name
        context['globalField'] = forms.CharField(max_length=20)
        user_name1 = User.objects.get(username=form.cleaned_data['username'])
        #context['name_of_user'] = 
        context['name_of_user'] = new_user.first_name + " " + new_user.last_name 
    
        return render(request, 'globalStreamPage.html', context)
    else:
        context['error'] = forms.ValidationError("Invalid username/password")
        return render(request, 'login.html', context)
