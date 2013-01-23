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
