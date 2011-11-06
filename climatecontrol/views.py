from selbst.climatecontrol.models import Thermostat, ThermostatTemperatureSensor, WeatherLocation
from selbst.core.models import Signal, SignalValue, Sensor
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from dateutil import zoneinfo
from datetime import datetime, timedelta
import time
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
    hours = request.GET.get('hours', None)
    days = request.GET.get('days', None)
    weeks = request.GET.get('weeks', None)
    if hours:
        context['timeperiod'] = 'hours=%s' % hours
    elif days:
        context['timeperiod'] = 'days=%s' % days
    elif weeks:
        context['timeperiod'] = 'weeks=%s' % weeks
    else:
        context['timeperiod'] = 'days=1'
    return render_to_response('climatecontrol/charts.html', context)

def data(request):
    ids = request.GET.getlist('sids')

    start = request.GET.get('start', None)
    end = request.GET.get('end', datetime.now())
    hours = request.GET.get('hours', None)
    if not hours:
        days = request.GET.get('days', None)
        if days:
            hours = int(days)*24
    if not hours:
        weeks = request.GET.get('weeks', None)
        if weeks:
            hours = int(weeks)*24*7

    signals = Signal.objects.filter(pk__in=ids)
    resp = {}
    resp['signals'] = []
    for s in signals:
        if hours:
            start = datetime.now() - timedelta(hours=int(hours))
            time_series = s.signalvalue_set.filter(created__gte=start)
        elif start:
            time_series = s.signalvalue_set.filter(created__range(start, end))
        else:
            time_series = s.signalvalue_set.filter(created__lte=end)
        signal_data = {
            'name': unicode(s),
            'data': [{'t':int(time.mktime(d.created.replace(microsecond=0).timetuple())), 'v':d.value} for d in time_series],
            'type':s.value_type
        }
        resp['signals'].append(signal_data)
    return HttpResponse(json.dumps(resp), mimetype='application/javascript')

