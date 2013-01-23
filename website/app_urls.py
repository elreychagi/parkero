# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$','website.app_views.home'),
    url(r'^set_points/(?P<id>\d+)/(?P<puntos>\d+)/$','website.app_views.set_points'),
)
