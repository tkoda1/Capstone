from django import forms
from pillPopperPro.models import Pill
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from pytz import all_timezones
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import datetime

def generate_time_choices():
    times = []
    start_time = datetime.datetime(2000, 1, 1, 0, 0)
    while start_time.time() < datetime.time(23, 45):
        times.append((start_time.time().strftime('%H:%M'), start_time.time().strftime('%I:%M %p')))
        start_time += datetime.timedelta(minutes=15)
    return times

COMMON_TIMEZONES = [
    'UTC', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
    'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Rome',
    'Asia/Tokyo', 'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Singapore',
    'Australia/Sydney', 'Australia/Melbourne'
]

DAYS_OF_WEEK = [
    ('MO', 'Monday'),
    ('TU', 'Tuesday'),
    ('WE', 'Wednesday'),
    ('TH', 'Thursday'),
    ('FR', 'Friday'),
    ('SA', 'Saturday'),
    ('SU', 'Sunday'),
]

username_validator = RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username.')

class PillForm(forms.Form):
    name = forms.CharField(max_length=100)
    dosage = forms.IntegerField(min_value=1, max_value=9999)
    quantity_initial = forms.IntegerField(min_value=1, label='Quantity Initial')

    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    disposal_times = forms.MultipleChoiceField(
        choices=generate_time_choices(),
        widget=forms.SelectMultiple(attrs={'size': 10})
    )

    timezone = forms.ChoiceField(
        choices=[(tz, tz.replace('_', ' ')) for tz in COMMON_TIMEZONES],
        widget=forms.Select(attrs={'class': 'timezone-dropdown'})
    )

    image = forms.ImageField(required=False)

    class Meta:
        model = Pill
        fields = ('name', 'dosage', 'disposal_times', 'days_of_week', 'quantity_initial', 'pill_slot', 'image')


    def clean_name(self):
        name = self.cleaned_data['name']
        if not name or len(name.strip()) == 0:
            raise forms.ValidationError('Including a prescription name is required')
        return name.strip()

    def clean_dosage(self):
        dosage = self.cleaned_data['dosage']
        return dosage

    def clean_quantity_initial(self):
        quantity_initial = self.cleaned_data['quantity_initial']
        if quantity_initial > 30:
            raise forms.ValidationError('Please enter valid quantity. Cannot hold more than 30 pills')
        return quantity_initial

    def clean_disposal_times(self):
        disposal_times = self.cleaned_data.get('disposal_times', [])
        if not disposal_times:
            raise forms.ValidationError("Please select at least one disposal time.")
        return disposal_times
    
    def clean_days_of_week(self):
        days = self.cleaned_data.get('days_of_week', [])
        if not days:
            raise forms.ValidationError("Please select at least one day.")
        return days


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, validators=[username_validator])

    password = forms.CharField(min_length=8, max_length=128, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid credentials.")
            if not user.is_active:
                raise forms.ValidationError("Account is inactive.")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, validators=[username_validator])
    password = forms.CharField(min_length=8, max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=8, max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('caretaker', 'Caretaker')])  # new!

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is not available.")
        return username

