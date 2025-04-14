
from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, body, user_email):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [ user_email ],
        fail_silently=False,
    )