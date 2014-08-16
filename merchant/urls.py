from django.conf.urls import patterns, url
from merchant.views import *

urlpatterns = patterns('',

	url(r'^list/$',merchant_list),	
    url(r'^detail/(?P<merchant_id>\d+)/$',merchant_detail),
    url(r'^location/amap/(?P<merchant_id>\d+)$',merchant_amap_location),
    url(r'^location/baidu/(?P<merchant_id>\d+)$',merchant_baidu_location),
    url(r'^distance/$',merchant_distance),
    url(r'^nearest/json/$',merchant_nearest_json),
    url(r'^detail/json/$',merchant_detail_json),
    url(r'^sort/json/$',merchant_sort_json),
    url(r'^city/json/$',merchant_city_json),
    url(r'^city/detail/json/$',merchant_city_detail_json),
    url(r'^fans/add/$',merchant_fans_add),
    url(r'^fans/cancel/$',merchant_fans_cancel),
    url(r'^fans/json/$',merchant_fans_json),
    )