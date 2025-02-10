from django.db import models

class Pill(models.Model):
    name = models.CharField(max_length=200)
    dosage = models.IntegerField() # in miligrams
    disposal_time = models.TimeField()
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()