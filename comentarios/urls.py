# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^set_comment/(?P<id>\d+)/$', 'comentarios.views.set_comentario'),
    url(r'^get_comments/(?P<id>\d+)', 'comentarios.views.get_comentarios'),
)
