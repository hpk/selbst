from django.db import models
from django_extensions.db.models import TimeStampedModel


SIGNAL_VALUE_TYPES = (
        ('real', 'Real'),
        ('int', 'Multi-State'),
        ('bool', 'Boolean'))

class Room(TimeStampedModel):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Sensor(TimeStampedModel):
    name = models.CharField(max_length=128)
    room = models.ForeignKey(Room, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Signal(TimeStampedModel):
    sensor = models.ForeignKey(Sensor, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    value_type = models.CharField(choices=SIGNAL_VALUE_TYPES, max_length=16)

    def __unicode__(self):
        if self.sensor:
            return self.sensor.name
        else:
            return self.name

class SignalValue(models.Model):
    signal = models.ForeignKey(Signal)
    real_value = models.FloatField(null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    bool_value = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def value(self):
        return getattr(self, '%s_value' % self.signal.value_type)

    def set_value(self, val):
        setattr(self, '%s_value' % self.signal.value_type, val)

    def __unicode__(self):
        return '[%s] %s : %s' % (self.signal, self.created, self.value)

class Actuator(TimeStampedModel):
    name = models.CharField(max_length=128)
    room = models.ForeignKey(Room, null=True, blank=True)
