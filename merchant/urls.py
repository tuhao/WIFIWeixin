from django.conf.urls import patterns, url
from merchant.views import *

urlpatterns = patterns('',

	url(r'^list/$',merchant_list),	
    url(r'^detail/(?P<merchant_id>\d+)/$',merchant_detail),
    url(r'^location/amap/(?P<merchant_id>\d+)$',merchant_amap_location),
    url(r'^location/baidu/(?P<merchant_id>\d+)$',merchant_baidu_location),
    url(r'^distance/$',merchant_distance),
    url(r'^nearest/(?P<scale>\d+\.?\d+)/$',merchant_nearest),
    )