from django.conf import settings
from django.db import models
import datetime
from django.contrib.auth.models import User

class Pill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=200)
    dosage = models.IntegerField()
    disposal_times = models.JSONField(default=list)  
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()
    pill_slot = models.IntegerField(default=0)
    # slot_angle = models.IntegerField(default=0)
    taken_today = models.IntegerField(default=0)
    timezone = models.CharField(max_length=50, default="UTC")  
    image = models.ImageField(upload_to="pill_images/", null=True, blank=True, default="pill.jpeg")  

    taken_times = models.JSONField(default=list)

    def __str__(self):
        return f"Pill id={self.id} | User: {self.user} | {self.name} | Time Zone: {self.timezone}"

    def add_taken_time(self):
        now = datetime.datetime.now().isoformat()  
        self.taken_times.append(now)  
        
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        self.taken_times = [
            time for time in self.taken_times 
            if datetime.datetime.fromisoformat(time) >= seven_days_ago
        ]

        self.save()
    
    def get_taken_times(self):
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        return [
            time for time in self.taken_times 
            if datetime.datetime.fromisoformat(time) >= seven_days_ago
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default="UTC")

    def __str__(self):
        return f"{self.user.username} - {self.timezone}"