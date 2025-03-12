from django.db import models

class Pill(models.Model):
    name = models.CharField(max_length=200)
    dosage = models.IntegerField() # in miligrams
    disposal_times = models.JSONField(default=list)  #new list
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()
    pill_slot = models.IntegerField(default=0)
    taken_today = models.IntegerField(default=0) # number of times taken today

    def __str__(self):
        return f"""Pill id={self.id}
                name={self.name} 
                dosage={self.dosage} 
                disposal_times={self.disposal_times} 
                quantity_initial={self.quantity_initial} 
                quantity_remaining={self.quantity_remaining}
                taken_today={self.quantity_remaining}"""