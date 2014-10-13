from django.conf.urls import patterns, url
from banner.views import *

urlpatterns = patterns('',
    
    url(r'^$',ads),
)
