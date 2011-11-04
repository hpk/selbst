from django.contrib import admin
from selbst.core.models import Room, Sensor, Signal, SignalValue, Actuator

admin.site.register(Room)
admin.site.register(Signal)
admin.site.register(Sensor)
admin.site.register(SignalValue)
admin.site.register(Actuator)

