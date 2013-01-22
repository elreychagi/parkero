# -*- coding: utf-8 -*-
import json
from django.db import connection
from django.http import HttpResponse
from geo.models import PosicionCliente
from usuarios.models import Estacionamiento
from usuarios.permisos import *

@user_passes_test(es_cliente, login_url='/')
def buscar_estacionmientos(request):
    lat = float(request.GET['lat'])
    long = float(request.GET['long'])
    radio = 10
    unidad_distancia = 6371

    posicion_cliente = PosicionCliente(cliente=request.user.cliente,
                        latitud=lat,
                        longitud=long)
    posicion_cliente.primero = True if 'recarga' not in request.GET else False
    posicion_cliente.save()
    cursor = connection.cursor()

    sql = """SELECT usuariobase_ptr_id AS id, latitud, longitud
             FROM usuarios_estacionamiento WHERE (%f * acos( cos( radians(%f) ) * cos( radians( latitud ) ) *
             cos( radians( longitud ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitud ) ) ) ) < %d
        """ % (unidad_distancia, lat, long, lat, int(radio))

    cursor.execute(sql)
    ids = [row[0] for row in cursor.fetchall()]

    parkings =[x.to_dict() for x in Estacionamiento.objects.all().filter(id__in=ids, activo=True)]
    return HttpResponse(json.dumps({'success' : True, 'parkings' : parkings}), mimetype='application/json')