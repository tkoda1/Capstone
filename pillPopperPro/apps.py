from django.apps import AppConfig
import sys
import logging

class PillpopperproConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pillPopperPro'

    def ready(self):
        # Skip DB-dependent logic during manage.py commands like migrate, makemigrations, etc.
        if any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell']):
            return

        try:
            from django_celery_beat.models import PeriodicTask, CrontabSchedule
            from django.db import connection
            from django.utils.timezone import now
            import json

            # Ensure the table exists before querying
            if 'django_celery_beat_periodictask' in connection.introspection.table_names():
                if not PeriodicTask.objects.filter(name='Send Notification Email').exists():
                    schedule, _ = CrontabSchedule.objects.get_or_create(
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
                        kwargs=json.dumps({})
                    )
        except Exception as e:
            logging.warning(f"Could not set up PeriodicTask: {e}")
