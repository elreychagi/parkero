# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^login/$','usuarios.views.login'),
    url(r'^logout/$','usuarios.views.logout'),

    url(r'^twitter_connect/$','usuarios.views.twitter_connect'),
    url(r'^twitter_callback/$','usuarios.views.twitter_callback'),
    url(r'^facebook_connect/$','usuarios.views.facebook_connect'),
    url(r'^facebook_callback/$','usuarios.views.facebook_callback'),

    url(r'^admin/crear_estacionamiento/$','usuarios.views.crear_estacionamiento'),
    url(r'^admin/listar_estacionamientos/(?P<page>\d+)?','usuarios.views.listar_estacionamientos'),
    url(r'^admin/editar_estacionamiento/(?P<id>\d+)/$','usuarios.views.editar_estacionamiento'),
    url(r'^admin/eliminar_estacionamiento/(?P<id>\d+)/$','usuarios.views.eliminar_estacionamiento'),

    url(r'^admin/listar_comentarios/(?P<park>\d+)/(?P<page>\d+)?','usuarios.views.listar_comentarios'),
    url(r'^admin/eliminar_comentario/(?P<id>\d+)/(?P<id_comentario>\d+)/$','usuarios.views.eliminar_comentario'),

    url(r'^admin/listar_usuarios/(?P<page>\d+)?','usuarios.views.listar_usuarios'),
    url(r'^admin/eliminar_usuario/(?P<id>\d+)/$','usuarios.views.eliminar_usuario'),

    url(r'^admin/editar_estacionamiento/(?P<id>\d+)/$','usuarios.views.editar_estacionamiento'),

    url(r'^park/editar_estacionamiento/$','usuarios.views.editar_estacionamiento'),
    url(r'^park/listar_comentarios/(?P<park>\d+)/(?P<page>\d+)?','usuarios.views.listar_comentarios'),
    url(r'^park/denunciar_comentario/(?P<id>\d+)/$','usuarios.views.denunciar_comentario'),
)
