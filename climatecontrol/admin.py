from django.contrib import admin
from selbst.climatecontrol.models import Thermostat, ThermostatTemperatureSensor, RecurringWeeklySetpoint, ScheduledHoldSetpoint

admin.site.register(Thermostat)
admin.site.register(ThermostatTemperatureSensor)
admin.site.register(RecurringWeeklySetpoint)
admin.site.register(ScheduledHoldSetpoint)
