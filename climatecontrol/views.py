from selbst.climatecontrol.models import Thermostat, ThermostatTemperatureSensor
from selbst.core.models import Signal, SignalValue, Sensor
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json

def charts(request):
    context = {}
    return render_to_response('climatecontrol/charts.html', context)

def data(request):
    therm = Thermostat.objects.all()[0]
    sensors = therm.thermostattemperaturesensor_set.all()
    signals = []
    for s in sensors:
        for sig in s.signal_set.all():
            signals.append(sig)
    signals.append(Signal.objects.get(name='Heat On'))
    signals.append(Signal.objects.get(name='Cool On'))
    signals.append(Signal.objects.get(name='Temperature Setpoint'))
    print sensors
    print signals

    resp = {}
    resp['signals'] = []
    for s in signals:
        time_series = s.signalvalue_set.order_by('created').all()
        signal_data = {
            'name': unicode(s),
            'data': [{'t':d.created.replace(microsecond=0).isoformat(), 'v':d.value} for d in time_series],
            'type':s.value_type
        }
        resp['signals'].append(signal_data)
    return HttpResponse(json.dumps(resp), mimetype='application/javascript')
