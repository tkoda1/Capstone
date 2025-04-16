from django.apps import AppConfig

class PillpopperproConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pillPopperPro'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        from django.utils.timezone import now
        import json

        # Avoid duplicates on restart
        if not PeriodicTask.objects.filter(name='Send Notification Email').exists():
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute='58',
                hour='*',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
            )

            PeriodicTask.objects.create(
                crontab=schedule,
                name='Send Notification Email',
                task='pillPopperPro.tasks.reset_taken_today',
                start_time=now(),
                enabled=True,
                kwargs=json.dumps({})  # optional args if your task takes inputs
            )