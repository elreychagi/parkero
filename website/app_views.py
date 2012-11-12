# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from users.permisos import *

from users.permisos import *

@user_passes_test(social_user, login_url='/')
def home(request):
    data = {}
    retorno = render_to_response("app/index.html", data, context_instance=RequestContext(request))
    return retorno

