# https://chatgpt.com/share/67fd3a14-42cc-8000-a0c9-61af969a7faf

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from .models import Pill, UserProfile
from .twilio_sms import send_sms
from .email import send_email
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import date


@shared_task
def reset_taken_today():
    now_utc = timezone.now()

    print('Running reset taken today')
    for userprofile in UserProfile.objects.all():
        user = userprofile.user

        caretakers = userprofile.caretakers.all()
        pills = Pill.objects.filter(user=user)
        pills_not_taken = []
        print(user.username)

        # find which pills the user hasn't taken today, and reset any if taken
        for pill in pills:
            pill_tz = ZoneInfo(pill.timezone)
            local_time = now_utc.astimezone(pill_tz)

            if (local_time.hour == 23) and (local_time.minute >= 58):
                if pill.taken_today == 0:
                    pills_not_taken.append(pill.name)
                    print(f'User has not taken pill {pill.name}')
                else:
                    pill.taken_today = 0
                    pill.save()
                    print(f'User has taken pill {pill}')

        # send email to user and caregivers if did not take all medication
        if pills_not_taken != []:
            print(caretakers)
            user_subject = 'Alert: failure to take medication'
            user_body = f"""Hello {user.get_full_name()},\n
                    You have not taken the following medications on {date.today()}: {', '.join(pills_not_taken)}\n
                    PillPopperPro Team"""
            user_email = user.email
            send_email(user_subject, user_body, user_email)
            caretaker_subject = 'Alert: patient failure to take medication'
            for caretaker in caretakers:
                print(caretaker)
                caretaker_body = f"""Hello {caretaker.get_full_name()},\n
                    You have not taken the following medications on {date.today()}: {', '.join(pills_not_taken)}\n
                    PillPopperPro Team"""
                caretaker_email = caretaker.email
                send_email(caretaker_subject, caretaker_body, caretaker_email)
