from django.conf.urls import patterns, url
from merchant.views import *

urlpatterns = patterns('',

	url(r'^list/$',merchant_list),	
    url(r'^detail/(?P<merchant_id>\d+)/$',merchant_detail),
    url(r'^location/(?P<merchant_id>\d+)$',merchant_location),
    url(r'^distance/$',merchant_distance),
    )