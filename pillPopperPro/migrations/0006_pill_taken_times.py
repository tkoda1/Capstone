# Generated by Django 5.1.6 on 2025-03-19 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillPopperPro', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='pill',
            name='taken_times',
            field=models.JSONField(default=list),
        ),
    ]
