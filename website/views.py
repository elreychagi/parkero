# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from usuarios.permisos import usuario_autenticado

def home(request):
    """
    Home de la aplicacion
    """
    data = {}
    if usuario_autenticado(request):
        data['usuario'] = request.user
    retorno = render_to_response("index.html", data, context_instance=RequestContext(request))
    return retorno
