from django.db import models
from django.utils import timezone

class BusData(models.Model):
    bus_number = models.CharField(max_length=20, default='Unknown')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    fuel_percent = models.FloatField(null=True, blank=True)
    fuel_level = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bus {self.bus_number} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


