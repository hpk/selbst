from django.db import models
from core.models import Signal, SignalValue, Sensor, SIGNAL_VALUE_TYPES

class PersonLocation(models.Model):
    name = models.CharField(max_length=32)
    device_udid = models.CharField(max_length=40)
    reported_time = models.DateTimeField(auto_now=True)

    altitude = models.FloatField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    accuracy = models.FloatField()
    speed = models.FloatField()
    heading = models.FloatField()

    at_home = models.BooleanField(default=True)


