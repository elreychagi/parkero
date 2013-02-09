# -*- coding: utf-8 -*-
from django.db.models import Avg

from django.shortcuts import render_to_response
from django.template import RequestContext
from comentarios.models import Puntos
from usuarios.permisos import *
from django.core.context_processors import csrf

@user_passes_test(es_cliente, login_url='/')
def home(request):
    """
    Vista del home de le aplicación en la que se muestra el mapa
    """
    data = {}
    data.update(csrf(request))
    retorno = render_to_response("app/index.html", data, context_instance=RequestContext(request))
    return retorno

@user_passes_test(es_cliente, login_url='/')
def set_points(request, id, puntos):
    """
    Servicio para puntear los estacionamientos
    """
    puntos = int(puntos)
    if puntos > 5 or puntos < 1:
        return HttpResponse(json.dumps({'success' : False, 'cause' : 'puntaje de 1-5'}), mimetype='application/json')
    try:
        estacionamiento = Estacionamiento.objects.get(pk=id)
        existe_puntos = Puntos.objects.all().filter(estacionamiento=estacionamiento, cliente=request.user.cliente).exists()
        if not existe_puntos:
            punto = Puntos(estacionamiento=estacionamiento,
                            cliente=request.user.cliente,
                            puntos=puntos)
            punto.save()
            puntos_avg = Puntos.objects.all().filter(estacionamiento=estacionamiento).aggregate(Avg('puntos'))['puntos__avg']
            return HttpResponse(json.dumps({'success' : True,
                                            'puntos' : int(round(puntos_avg, 2)) if puntos_avg is not None else 0}),
                                mimetype='application/json')
        else:
            return HttpResponse(json.dumps({'success' : False, 'cause' : 'exist'}), mimetype='application/json')
    except:
        pass
    return HttpResponse(json.dumps({'success' : False, 'cause' : 'error inesperado'}), mimetype='application/json')