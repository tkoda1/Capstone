
from django.core.mail import send_mail
from django.conf import settings
from .contants import DAYS_OF_WEEK, DISPOSAL_TIMES
import textwrap
from datetime import datetime

def send_email(subject, body, user_email):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [ user_email ],
        fail_silently=False,
    )

def get_new_pill_email_body(pill):
    days_of_week = []
    disposal_times = []
    
    for value, label in DAYS_OF_WEEK:
        if value in pill.days_of_week:
            days_of_week.append(label)
    
    for value, label in DISPOSAL_TIMES:
        if value in pill.disposal_times:
            disposal_times.append(label)

    days_of_week_str = ', '.join(days_of_week)
    disposal_times_str = ', '.join(disposal_times)

    body = textwrap.dedent(f"""\
            Hello {pill.user.get_full_name()},

            You have created a new pill with the following information: 

            Pill Name: {pill.name}
            Dosage: {pill.dosage}
            Disposal times: {disposal_times_str}
            Days of week to take medication: {days_of_week_str}
            Quantity initial: {pill.quantity_initial}
            Quantity remaining: {pill.quantity_remaining}
            Timezone: {pill.timezone}
            Stored in pill compartment {pill.pill_slot}

            Please make sure to take your medication as prescribed.

            PillPopperPro Team
            Sent on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}""")
    return body