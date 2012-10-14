from django.http import HttpResponse
import time

__author__ = 'Isaac Casado'

def inicio(request):
    suma = 2 + 2

    return HttpResponse('Prueba %d'%suma)

def ahora(request):

    varget = request.GET.get('primero', None)

    if varget is not None:
        retorno = 'Pasaron %s por GET'%varget
    else:
        retorno = 'Sin variables'

    return HttpResponse(retorno)