# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^buscar_estacionmientos/$','geo.views.buscar_estacionmientos'),
)
