# Generated by Django 5.1.6 on 2025-03-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillPopperPro', '0007_pill_taken_today'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pill',
            name='disposal_time',
        ),
        migrations.AddField(
            model_name='pill',
            name='disposal_times',
            field=models.JSONField(default=list),
        ),
    ]
