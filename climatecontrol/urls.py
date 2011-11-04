from django.conf.urls.defaults import *

urlpatterns = patterns('selbst.climatecontrol.views',
    (r'^charts/?', 'charts'),
    (r'^data/?', 'data'),
)
