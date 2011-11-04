from selbst.climatecontrol.models import Thermostat, ThermostatTemperatureSensor, WeatherLocation
from selbst.core.models import Signal, SignalValue, Sensor
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from dateutil import zoneinfo
from datetime import datetime
from selbst.lib.thermostat import ThermostatClient

def control(request):
    therm = Thermostat.objects.all()[0]
    client = ThermostatClient(therm.ip_address)
    if request.method == 'POST':
        pass
    else:
        pass

def charts(request):
    context = {}
    therm = Thermostat.objects.all()[0]
    sensors = therm.thermostattemperaturesensor_set.all()
    signals = []
    for s in sensors:
        for sig in s.signal_set.all():
            signals.append(sig)
    for s in WeatherLocation.objects.all():
        for sig in s.signal_set.all():
            signals.append(sig)
    context['default_sigs'] = signals + [Signal.objects.get(name='Temperature Setpoint')]
    all_sigs = [s for s in context['default_sigs']]
    all_sigs.append(Signal.objects.get(name='Heat On'))
    all_sigs.append(Signal.objects.get(name='Cool On'))
    context['all_sigs'] = all_sigs
    return render_to_response('climatecontrol/charts.html', context)

def data(request):
    timezone = zoneinfo.gettz('US/Central')
    utc = zoneinfo.gettz('UTC')
    ids = request.GET.getlist('sids')

    start = request.GET.get('start', None)
    end = request.GET.get('end', datetime.now())

    signals = Signal.objects.filter(pk__in=ids)
    resp = {}
    resp['signals'] = []
    for s in signals:
        if start:
            time_series = s.signalvalue_set.filter(created__range(start, end))
        else:
            time_series = s.signalvalue_set.filter(created__lte=end)
        signal_data = {
            'name': unicode(s),
            'data': [{'t':d.created.replace(microsecond=0).isoformat(), 'v':d.value} for d in time_series],
            'type':s.value_type
        }
        resp['signals'].append(signal_data)
    return HttpResponse(json.dumps(resp), mimetype='application/javascript')

