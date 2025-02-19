from django import forms
from pillPopperPro.models import Pill

class PillForm(forms.Form):
    class Meta:
        model = Pill
        fields = ('name', 'dosage', 'disposal_time', 'quantity_initial')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise forms.ValidationError('Prescription name is too long')
        if not name or len(name) == 0:
            raise forms.ValidationError('Including a prescription name is requred')
        return name

    def clean_dosage(self):
        dosage = self.cleaned_data['dosage']
        if dosage < 1 or dosage > 9999:
            raise forms.ValidationError('Please re-enter a valid dosage')
        return dosage

    def clean_quantity_initial(self):
        quantity_initial = self.cleaned_data['quantity_initial']
        if quantity_initial != 30: # only accepting a 30 day supply
            raise forms.ValidationError('Please enter valid quantity')
        return quantity_initial
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=20)
    password  = forms.CharField(max_length=200,
                                 label='Password', 
                                 widget=forms.PasswordInput())
    confirm_password  = forms.CharField(max_length=200,
                                 label='Confirm password',  
                                 widget=forms.PasswordInput())

    
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username