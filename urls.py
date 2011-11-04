from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^climate/', include('selbst.climatecontrol.urls')),
    #url(r'^core/', include('selbst.core.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
