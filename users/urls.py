# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^twitter_connect/$','users.views.twitter_connect'),
    url(r'^twitter_callback/$','users.views.twitter_callback'),
    url(r'^facebook_connect/$','users.views.facebook_connect'),
    url(r'^facebook_callback/$','users.views.facebook_callback'),

)
