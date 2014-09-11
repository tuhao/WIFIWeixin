from django.conf.urls import patterns, url
from upgrade.views import *

urlpatterns = patterns('',

	url(r'^apk/$',apk_version),
	url(r'^redirect/$',redirect_test),


)