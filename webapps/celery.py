import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps.settings')

app = Celery('webapps')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
