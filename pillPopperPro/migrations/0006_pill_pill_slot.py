# Generated by Django 5.1.6 on 2025-02-24 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillPopperPro', '0005_remove_pill_pill_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='pill',
            name='pill_slot',
            field=models.IntegerField(default=0),
        ),
    ]
