from selbst.core.models import Signal, SignalValue, Sensor
from selbst.location.models import PersonLocation
from selbst.lib.utils import distance_meters
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

def report(request):
    deviceid = request.GET.get('deviceid')
    try:
        ploc = PersonLocation.objects.get(device_udid=deviceid)
    except PersonLocation.DoesNotExist:
        ploc = PersonLocation(device_udid=deviceid, name="Unnamed Person")

    ploc.latitude = float(request.GET.get('lat'))
    ploc.longitude = float(request.GET.get('lon'))
    ploc.altitude = float(request.GET.get('altitude'))
    ploc.speed = float(request.GET.get('speed'))
    ploc.heading = float(request.GET.get('heading'))
    ploc.accuracy = float(request.GET.get('hacc'))

    home = settings.HOME_LOCATION
    d_meters = distance_meters(ploc.latitude, ploc.longitude, home['latitude'], home['longitude'])

    if d_meters - ploc.accuracy - home['radius'] > 0:
        ploc.at_home = False
    else:
        ploc.at_home = True
    ploc.save()

    sig = Signal.objects.get_or_create("%s at home" % ploc.name, value_type='bool')
    sv = SignalValue(signal=sig)
    sv.set_value(plot.at_home)
    sv.save()
    
    return HttpResponse('')
