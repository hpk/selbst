from selbst.climatecontrol.models import Thermostat, ThermostatTemperatureSensor, WeatherLocation
from selbst.core.models import Signal, SignalValue, Sensor
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
import json
from dateutil import zoneinfo
from datetime import datetime, timedelta
import time
from selbst.lib.thermostat import ThermostatClient

@login_required
def control(request):
    therm = Thermostat.objects.all()[0]
    client = ThermostatClient(therm.ip_address)
    if request.method == 'POST':
        temp_setpoint = request.POST.get('temp')
        hold = request.POST.get('hold')
        params = {'a_heat': float(temp_setpoint)}
        client.send('/tstat', params)
        return HttpResponseRedirect('/climate')
    else:
        context = {}
        context.update(csrf(request))
        cur_state = client.get('/tstat')
        context['current_temp'] = cur_state.get('temp', None)
        context['setpoint'] = cur_state.get('t_heat', None)
        context['heat_on'] = cur_state.get('tstate') == 1
        return render_to_response('climatecontrol/index.html', context)

@login_required
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

    resp = {}
    resp_signals = {}

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
            'name': s.name,
            'data': [{'t': int(time.mktime(v[0].replace(microsecond=0).timetuple())), 'v': v[1]} for v in time_series.values_list('created', 'value')]
            'type': s.value_type
        }
        resp['signals'].append(signal_data)
    return HttpResponse(json.dumps(resp), mimetype='application/javascript')

