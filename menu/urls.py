from django.conf.urls import patterns, url
from menu.views import *

urlpatterns = patterns('',
    
    url(r'^create_menu/$',create_menu),

    url(r'^delete_menu/$',delete_menu),
)
