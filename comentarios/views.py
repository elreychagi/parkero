# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from comentarios.models import Comentarios
from usuarios.models import Estacionamiento
from usuarios.permisos import user_passes_test
from usuarios.permisos import *

@user_passes_test(es_cliente, login_url='/')
def set_comentario(request, id):
    try:
        if 'contenido' not in request.POST or request.POST['contenido'] == '':
            return HttpResponse(json.dumps({'success' : False, 'cause' : 'contenido vacio'}), mimetype='application/json')

        estacionamiento = Estacionamiento.objects.get(pk=id)
        comentario = Comentarios(estacionamiento=estacionamiento,
                                cliente=request.user.cliente,
                                contenido=request.POST['contenido'])
        comentario.save()

        return HttpResponse(json.dumps({'success' : True, 'comentario' : comentario.to_dict(cliente=request.user.cliente)}), mimetype='application/json')
    except:
        pass
    return HttpResponse(json.dumps({'success' : False, 'cause' : 'error inesperado'}), mimetype='application/json')

@user_passes_test(es_cliente, login_url='/')
def get_comentarios(request, id):
    try:
        offset = 0 if 'offset' not in request.GET else request.GET['offset']
        comentarios = [x.to_dict() for x in Comentarios.objects.all().filter(estacionamiento=id)]
        return HttpResponse(json.dumps({'success' : True, 'comentarios' : comentarios}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success' : True}), mimetype='application/json')