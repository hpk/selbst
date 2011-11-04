from twisted.internet import task, reactor
import requests
import json
from datetime import datetime, timedelta
from selbst.core.models import Signal, SignalValue
from selbst.climatecontrol.models import Thermostat, RecurringWeeklySetpoint, ThermostatTemperatureSensor, ScheduledHoldSetpoint
from operator import attrgetter

def post(path, data):
    return json.loads(requests.post(path, json.dumps(data)).content)

def get(path):
    return json.loads(requests.get(path).content)

def _get_date_this_week(recur_setpoint, now=None):
    if not now:
        now = datetime.now()
    wd_diff = recur_setpoint.day_of_week - now.weekday()
    date_this_week = now + timedelta(days=wd_diff)
    return date_this_week.replace(hour=recur_setpoint.hour, minute=recur_setpoint.minute)

def _get_signal(name=None, sensor=None):
    if name:
        signals = Signal.objects.filter(name=name)
    else:
        signals = Signal.objects.filter(sensor=sensor)
    if not signals:
        return None
    else:
        return signals[0]

def _save_datapoint(signal, value):
    sv = SignalValue(signal=signal)
    sv.set_value(value)
    sv.save()

def event_loop():
    now = datetime.now()
    therm = Thermostat.objects.all()[0]
    url = "http://%s/tstat" % therm.ip_address
    cur_state = get(url)
    cur_temp = cur_state.get('temp', None)
    cur_operating_mode = cur_state.get('tmode', 0)
    cur_hvac_state = cur_state.get('tstate', 0)
    is_override = False if cur_state.get('override', 0) == 0 else True
    is_hold = False if cur_state.get('hold', 0) == 0 else True
    heat_setpoint = cur_state.get('t_heat', None)
    cool_setpoint = cur_state.get('t_cool', None)

    cur_running_setpoint = heat_setpoint if cur_operating_mode == 1 else cool_setpoint

    # Save data as signals
    tempsensor = ThermostatTemperatureSensor.objects.filter(thermostat=therm)[0]
    indoor_temp_signal = _get_signal(sensor=tempsensor) or Signal.objects.create(sensor=tempsensor, value_type='real')
    heat_on_signal = _get_signal(name='Heat On') or Signal.objects.create(name='Heat On', value_type='bool')
    cool_on_signal = _get_signal(name='Cool On') or Signal.objects.create(name='Cool On', value_type='bool')
    setpoint_signal = _get_signal(name='Temperature Setpoint') or Signal.objects.create(name='Temperature Setpoint', value_type='real')
    _save_datapoint(indoor_temp_signal, cur_temp)
    _save_datapoint(heat_on_signal, cur_hvac_state == 1)
    _save_datapoint(cool_on_signal, cur_hvac_state == 2)

    # Look up latest weekly recurring setpoint to use
    recurring_setpoints = RecurringWeeklySetpoint.objects.all()
    sorted_recurring = sorted(recurring_setpoints, key=attrgetter('day_of_week', 'hour', 'minute'))
    recurring_setpoint = None
    for s in sorted_recurring:
        date_this_week = _get_date_this_week(s, now=now)
        if date_this_week < now:
            recurring_setpoint = s

    # See if we have any scheduled hold setpoints
    # Doesn't make sense to have overlapping hold setpoints, so pick the first one we find
    hold_setpoints = ScheduledHoldSetpoint.objects.filter(start__lte=now, end__gte=now)
    hold_setpoint = hold_setpoints[0] if hold_setpoints else None

    # Figure out which setpoint to use
    # Scheduled hold setpoints trump recurring weekly setpoints,
    # and manual override (from thermostat panel or web interface) trump all
    if recurring_setpoint:
        last_recurring_setpoint = therm.last_recurring_setpoint
        if not last_recurring_setpoint:
            switch_periods = True
        else:
            if _get_date_this_week(recurring_setpoint, now=now) > _get_date_this_week(last_recurring_setpoint, now=now):
                switch_periods = True
            else:
                switch_periods = False

    if hold_setpoint:
        last_hold_setpoint = therm.last_scheduled_setpoint
        if last_hold_setpoint is not hold_setpoint:
            switch_periods = True

    therm.last_recurring_setpoint = recurring_setpoint
    therm.last_scheduled_setpoint = hold_setpoint
    therm.save()

    temp_to_set = None
    if recurring_setpoint:
        temp_to_set = recurring_setpoint.setpoint
        new_mode = recurring_setpoint.mode
    if hold_setpoint:
        temp_to_set = hold_setpoint.setpoint
        new_mode = hold_setpoint.mode
    if is_override and not switch_periods:
        temp_to_set = None

    if temp_to_set and temp_to_set != cur_running_setpoint:
        if new_mode == 'auto':
            new_mode = therm.mode
        if new_mode == 'heat':
            params = {'a_heat': temp_to_set, 'hold': 1, 'a_mode': 1}
        elif new_mode == 'cool':
            params = {'a_cool': temp_to_set, 'hold': 1, 'a_mode': 1}
        if new_mode != therm.mode:
            params.update({'tmode': 1 if new_mode == 'heat' else 2})
        post(url, params)
        # TODO: Handle auto mode
        _save_datapoint(setpoint_signal, temp_to_set)
    else:
        if cur_running_setpoint:
            _save_datapoint(setpoint_signal, cur_running_setpoint)


def start_daemon(*args, **kwargs):
    l = task.LoopingCall(event_loop)
    l.start(60.0) # Run every minute
