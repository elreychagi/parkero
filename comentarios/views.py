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
    if 0==0:
        offset = 0 if 'offset' not in request.GET else int(request.GET['offset'])
        limit = 5
        comentarios = [x.to_dict(admin=False, cliente=request.user.cliente) for x in Comentarios.objects.all().filter(estacionamiento=id)[offset:limit + offset]]
        return HttpResponse(json.dumps({'success' : True, 'comentarios' : comentarios}), mimetype='application/json')
    '''except:
        return HttpResponse(json.dumps({'success' : False}), mimetype='application/json')'''