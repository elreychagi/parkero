# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^login/$','users.views.login'),
    url(r'^logout/$','users.views.logout'),

    url(r'^twitter_connect/$','users.views.twitter_connect'),
    url(r'^twitter_callback/$','users.views.twitter_callback'),
    url(r'^facebook_connect/$','users.views.facebook_connect'),
    url(r'^facebook_callback/$','users.views.facebook_callback'),

    url(r'^admin/crear_estacionamiento/$','users.views.new_parking'),
    url(r'^admin/listar_estacionamientos/(?P<page>\d+)?','users.views.list_parkings'),
    url(r'^admin/editar_estacionamiento/(?P<id>\d+)/$','users.views.edit_parking'),
    url(r'^admin/eliminar_estacionamiento/(?P<id>\d+)/$','users.views.delete_parking'),

    url(r'^admin/listar_comentarios/(?P<park>\d+)/(?P<page>\d+)?','users.views.list_comments'),
    url(r'^admin/eliminar_comentarios/(?P<id>\d+)/$','users.views.delete_comments'),
)
