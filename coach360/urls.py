'''
@author: lowcoupling
'''
from django.conf.urls.defaults import *

from spices.coach360 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<survey_id>\d+)/$', views.survey, name='survey'),
    url(r'^(?P<survey_id>\d+)/(?P<user_id>\d+)/$', views.usersurvey, name='usersurvey'),
    url(r'^results/$', views.indexresults, name='indexresults'),
    url(r'^(?P<survey_id>\d+)/results/$', views.surveyresults, name='surveyresults'),
    url(r'^(?P<survey_id>\d+)/(?P<user_id>\d+)/results/$', views.usersurveyresults, name='usersurveyresults'),
)
