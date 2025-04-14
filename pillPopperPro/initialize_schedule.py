from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now
import json

# Create crontab (23:59 every day)
# schedule, created = CrontabSchedule.objects.get_or_create(
#     minute='28',
#     hour='13',
#     day_of_week='*',
#     day_of_month='*',
#     month_of_year='*',
# )

# # Create the task
# PeriodicTask.objects.create(
#     crontab=schedule,
#     name='Reset pills each night',
#     task='pillPopperPro.tasks.reset_taken_today',
#     start_time=now(),
#     args=json.dumps([]),
# )


from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create or get a crontab schedule for every minute
schedule, created = CrontabSchedule.objects.get_or_create(
    minute='*',
    hour='*',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

# Create the periodic task
PeriodicTask.objects.create(
    crontab=schedule,
    name='Test task every minute',
    task='pillPopperPro.tasks.reset_taken_today',
    args=json.dumps([]),
)
