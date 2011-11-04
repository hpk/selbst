from django.db import models
from core.models import Signal, SignalValue, Sensor, SIGNAL_VALUE_TYPES

SETPOINT_MODES = (
        ('auto', 'Auto'),
        ('heat', 'Heat'),
        ('cool', 'Cool')
        )

DAY_OF_WEEK_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
        )


INT_TO_DAY = {
        6: 'Sunday',
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday'
        }

class Thermostat(models.Model):
    ip_address = models.IPAddressField()
    last_recurring_setpoint = models.ForeignKey('RecurringWeeklySetpoint', null=True, blank=True, related_name='thermostat_recurring_setpoint')
    last_scheduled_setpoint = models.ForeignKey('ScheduledHoldSetpoint', null=True, blank=True, related_name='thermostat_scheduled_setpoint')

    def __unicode__(self):
        return "Filtrete 3M-50 Radio Thermostat [%s]" % self.ip_address


class ThermostatTemperatureSensor(Sensor):
    thermostat = models.ForeignKey(Thermostat)


class TemperatureSetpoint(models.Model):
    # Can be specific to one thermostat, or apply to all
    thermostat = models.ForeignKey(Thermostat, null=True, blank=True)
    setpoint = models.FloatField()
    mode = models.CharField(choices=SETPOINT_MODES, max_length=4, default='auto')

    def __unicode__(self):
        return "%s: %s" % (self.mode, self.setpoint)


class RecurringWeeklySetpoint(TemperatureSetpoint):
    day_of_week = models.PositiveIntegerField(choices=DAY_OF_WEEK_CHOICES) # 0 is sunday, 6 is saturday
    hour = models.PositiveIntegerField(default=0) # 0 - 23
    minute = models.PositiveIntegerField(default=0) # 0 - 59

    def __unicode__(self):
        return "%s %2d:%2d : %s" % (INT_TO_DAY[self.day_of_week], self.hour, self.minute, self.setpoint)


class ScheduledHoldSetpoint(TemperatureSetpoint):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return "%s -> %s : %s" % (self.start, self.end, self.setpoint)


