from django.conf import settings
from django.db import models

class Pill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=200)
    dosage = models.IntegerField()
    disposal_times = models.JSONField(default=list)
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()
    pill_slot = models.IntegerField(default=0)
    taken_today = models.IntegerField(default=0)

    def __str__(self):
        return f"Pill id={self.id} | {self.user} | {self.name}"

