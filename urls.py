from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^coach360/', include('spices.coach360.urls', namespace='coach360')),
    url(r'^accounts/', include('spices.login.urls')),
    url(r'^admin/', include(admin.site.urls)),
  
)

# 
