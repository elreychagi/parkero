# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    data = {}
    retorno = render_to_response("index.html", data, context_instance=RequestContext(request))
    return retorno
