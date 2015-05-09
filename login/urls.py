from django.conf.urls.defaults import *

from spices.login import views

urlpatterns = patterns('',
    url(r'login', views.login_view, name='login'),
    url(r'logout', views.logout_view, name = 'logout'),
)
