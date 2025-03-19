from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Pill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=200)
    dosage = models.IntegerField()
    disposal_times = models.JSONField(default=list)  
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()
    pill_slot = models.IntegerField(default=0)
    taken_today = models.IntegerField(default=0)
    timezone = models.CharField(max_length=50, default="UTC")  
    image = models.ImageField(upload_to="pill_images/", null=True, blank=True, default="pill.jpeg")  

    def __str__(self):
        return f"Pill id={self.id} | User: {self.user} | {self.name} | Time Zone: {self.timezone}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default="UTC")

    def __str__(self):
        return f"{self.user.username} - {self.timezone}"