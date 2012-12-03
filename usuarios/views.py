# -*- coding: utf-8 -*-
import hashlib
import json
import urllib
import urlparse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import tweepy
from comentarios.models import Comentarios
from dalero.settings import TWITTER, FACEBOOK
from usuarios.forms import FormEstacionamiento
from usuarios.models import Estacionamiento, UsuarioBase, Cliente
from usuarios.permisos import *


def twitter_connect(request):
    """
    Inicio del proceso oauth de Twitter
    Se obtiene el request_token para luego redireccionar al usuario a la página para solicitar permiso de acceso
    Libreria tweepy
    """

    if 0==0:
        auth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'], TWITTER["CALLBACK"])
        redirect_url = auth.get_authorization_url()
        rkey = auth.request_token.key
        rsecret = auth.request_token.secret
        request.session['tw_rt'] = "%s::%s"%(rkey, rsecret)
        return HttpResponseRedirect(redirect_url)

    return HttpResponseRedirect('/?error_twitter')

def twitter_callback(request):
    """
    Una vez el usuario permise o no el acceso a su cuenta de Twitter esta vista revisa si concedio permisos o no
    En caso afirmativo busca a un usuario con ese id de Twitter para crear la sesion, de no existir crea al usuario
    """
    retorno = HttpResponseRedirect('/')
    if 0==0:
        s = request.session['tw_rt']
        tokens = s.split('::')
        request_token = tokens[0]
        request_secret = tokens[1]

        if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
            oauth_verifier = request.GET['oauth_verifier']
            oauth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'])
            oauth.set_request_token(request_token, request_secret)
            oauth.get_access_token(oauth_verifier)
            api = tweepy.API(oauth)
            tw_user = api.verify_credentials()
            try:
                cliente = Cliente.objects.get(twitter_id=tw_user.id)
                cliente.login(request)
            except Cliente.DoesNotExist:
                accesstoken = oauth.access_token.key
                secret = oauth.access_token.secret
                cliente = Cliente(nombre_usuario="%s_tc"%tw_user.screen_name,
                    twitter_id=tw_user.id,
                    twitter_accesstoken=accesstoken,
                    twitter_secrettoken=secret)
                cliente.save()
                cliente.login(request)
            retorno = HttpResponseRedirect('/app/')
    '''except:
        retorno = HttpResponseRedirect('/?error_twitter')'''
    del request.session['tw_rt']
    return retorno

def facebook_connect(request):
    """
    Inicio del proceso oauth de Facebook
    Se obtiene el request_token para luego redireccionar al usuario a la página para solicitar permiso de acceso
    """
    facebook_oauth = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=email,publish_stream,offline_access"\
                     %(FACEBOOK["KEY"],
                       FACEBOOK["CALLBACK"])
    return HttpResponseRedirect(facebook_oauth)

def facebook_callback(request):
    """
    Una vez el usuario permise o no el acceso a su cuenta de Facebook esta vista revisa si concedio permisos o no
    En caso afirmativo busca a un usuario con ese id de Facebook para crear la sesion, de no existir crea al usuario
    """
    code = None if 'code' not in request.GET else request.GET['code']
    retorno = HttpResponseRedirect('/?error_facebook')
    if 0==0:
        if code is not None:
            args = dict(client_id=FACEBOOK["KEY"],
                        redirect_uri=FACEBOOK["CALLBACK"],
                        client_secret=FACEBOOK["SECRET"],
                        code=code)
            response = urlparse.parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?%s"%urllib.urlencode(args)).read())

            access_token = response["access_token"][-1]

            if access_token is not None:
                fb_user = json.load(urllib.urlopen("https://graph.facebook.com/me?%s"%urllib.urlencode(dict(access_token=access_token))))
                if 'id' in fb_user:
                    try:
                        cliente = Cliente.objects.get(facebook_id=fb_user['id'])
                        cliente.login(request)
                    except Cliente.DoesNotExist:
                        cliente = Cliente(nombre_usuario="%s_fb"%fb_user['username'],
                            facebook_id=fb_user['id'],
                            facebook_accesstoken=access_token,
                            facebook_code=code)
                        cliente.save()
                        cliente.login(request)
                        request.session['tipo'] = 'cliente'
                    retorno = HttpResponseRedirect('/app/')
    """except:
        pass"""
    return retorno

@user_passes_test(es_administrador, login_url='/users/login/')
def crear_estacionamiento(request):
    """
    Vista para crear estacionamiento
    Se valida si existe un UsuarioBase con el email y nombre_usuario pasado (deben ser unicos)
    Se crea el password tipo nombre_usuario12345
    """
    errors = {}
    if request.method != 'POST':
        form = FormEstacionamiento()
    else:
        form = FormEstacionamiento(data=request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data

            if UsuarioBase.objects.all().filter(nombre_usuario=clean_data['nombre_usuario']).exists():
                errors = {'nombre_usuario' : {'as_text':'* Nombre de usuario usado'}}
            elif UsuarioBase.objects.all().filter(correo=clean_data['correo']).exists():
                errors = {'correo' : {'as_text':'* Correo electrónico usado'}}
            else:
                password = new_password(user=clean_data['nombre_usuario'])
                estacionamiento = Estacionamiento(
                    nombre_usuario=clean_data['nombre_usuario'],
                    password=password,
                    correo=clean_data['correo'],
                    descripcion=clean_data['descripcion'],
                    nombre=clean_data['nombre'],
                    latitud=clean_data['latitud'],
                    longitud=clean_data['longitud'],
                    motos=clean_data['motos'],
                    camiones=clean_data['camiones'],
                    sin_techo=clean_data['sin_techo'])
                estacionamiento.save()

                """msg = MIMEText(u"Bienvenido a Dalero.net su contrase&nacute;a de ingreso es %s"%password,'html')
                msg["From"] = "enydrueda@gmail.com"
                msg["To"] = estacionamiento.correo
                msg["Subject"] = "Bienvenido a Dalero.net"
                p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
                p.communicate(msg.as_string())"""
                return HttpResponseRedirect('/users/admin/listar_estacionamientos/')
        else:
            errors = form.errors
    return render_to_response('usuarios/crear_editar_estacionamiento.html', {'form' : form, 'errors' : errors}, context_instance=RequestContext(request))

@user_passes_test(es_administrador, login_url='/users/login/')
def listar_estacionamientos(request, page=1):
    """
    Vista para mostrar los estacionamientos registrados con paginacion
    """
    estacionamientos = Estacionamiento.objects.all()

    paginator = Paginator(estacionamientos, 20)
    
    try:
        page = int(page)
    except:
        page = 1

    try:
        pagina = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pagina = paginator.page(paginator.num_pages)

    pagination = {'object_list': [x.to_dict(admin=True) for x in pagina.object_list],
                          'has_prev': pagina.has_previous(),
                          'has_next': pagina.has_next(),
                          'prev_page': pagina.previous_page_number() if pagina.has_previous() else None,
                          'next_page': pagina.next_page_number() if pagina.has_next() else None,
                          'page': pagina.number,
                          'num_pages': pagina.paginator.num_pages,
    }
    return render_to_response('usuarios/listar_estacionamientos.html', {'pagination' : pagination,}, context_instance=RequestContext(request))

@user_passes_test(es_estacionamiento, login_url='/users/login/')
def editar_estacionamiento(request, id=None):
    """
    Vista para editar estacionamiento
    Podran usar esta vista tanto estacionamientos como administrador
    """
    errors = {}
    es_estac = Estacionamiento.objects.all().filter(usuariobase_ptr_id=request.user.id).exists()
    if 0==0:
        if es_estac:
            estacionamiento = request.user.estacionamiento
        else:
            estacionamiento = Estacionamiento.objects.get(pk=id)
        if request.method != 'POST':
            initial = {'nombre' : estacionamiento.nombre,
                       'nombre_usuario' : estacionamiento.nombre_usuario,
                       'correo' : estacionamiento.correo,
                       'descripcion' : estacionamiento.descripcion,
                       'motos' : estacionamiento.motos,
                       'camiones' : estacionamiento.camiones,
                       'sin_techo' : estacionamiento.sin_techo,
                       'id' : estacionamiento.id}
            if not es_estac:
                initial.update({'latitud' : estacionamiento.latitud,
                                'longitud' : estacionamiento.longitud,})
            form = FormEstacionamiento(initial=initial,
                                        edit=True,
                                        parking=es_estac)
        else:
            form = FormEstacionamiento(data=request.POST, edit=True, parking=es_estac)
            if form.is_valid():
                clean_data = form.cleaned_data
                if Estacionamiento.objects.all().exclude(pk=estacionamiento.id).filter(correo=clean_data['correo']).exists():
                    errors = {'correo' : {'as_text':'* Correo electrónico usado'}}
                else:
                    estacionamiento.descripcion = clean_data['descripcion']
                    estacionamiento.nombre = clean_data['nombre']
                    estacionamiento.motos = clean_data['motos']
                    estacionamiento.camiones = clean_data['camiones']
                    estacionamiento.sin_techo = clean_data['sin_techo']
                    if not es_estac:
                        estacionamiento.latitud = clean_data['latitud']
                        estacionamiento.longitud = clean_data['longitud']
                    estacionamiento.save()
            else:
                errors = form.errors
        return render_to_response('usuarios/crear_editar_estacionamiento.html',
            {'form' : form, 'errors' : errors, 'es_estacionamiento' : es_estac, 'estacionamiento' : estacionamiento},
            context_instance=RequestContext(request))
    '''except Estacionamiento.DoesNotExist:
        raise Http404()'''

@user_passes_test(es_administrador, login_url='/users/login/')
def eliminar_estacionamiento(request, id):
    """
    Vista para el soft delete de estacionamientos
    La misma permitira desactivar y activar
    """
    try:
        estacionamiento = Estacionamiento.objects.get(pk=id)
        estacionamiento.activo = not estacionamiento.activo
        estacionamiento.save()
        return HttpResponseRedirect('/users/admin/listar_estacionamientos/')
    except Estacionamiento.DoesNotExist:
        raise Http404()

@user_passes_test(es_estacionamiento, login_url='/users/login/')
def listar_comentarios(request, park, page=1):
    """
    Vista para listar los comentarios de un estacionamiento
    La misma podra ser usada por estacionamiento como por administrador
    """
    try:
        estacionamiento = Estacionamiento.objects.get(pk=park, activo=True)
        comments = Comentarios.objects.all().filter(estacionamiento__id=estacionamiento.id, cliente__activo=True)
        es_estac = Estacionamiento.objects.all().filter(usuariobase_ptr_id=request.user.id).exists()
        if es_estac and request.user.estacionamiento.id != estacionamiento.id:
            raise Http404()
        paginator = Paginator(comments, 20)

        try:
            page = int(page)
        except:
            page = 1

        try:
            comentarios = paginator.page(page)
        except (EmptyPage, InvalidPage):
            comentarios = paginator.page(paginator.num_pages)

        next_page = comentarios.next_page_number() if comentarios.has_next() else 0

        pagination = {'object_list': [x.to_dict(admin=True) for x in comentarios.object_list],
                      'has_prev': comentarios.has_previous(),
                      'has_next': comentarios.has_next(),
                      'prev_page': comentarios.previous_page_number() if comentarios.has_previous() else None,
                      'next_page': next_page if comentarios.has_next() else None,
                      'page': comentarios.number,
                      'num_pages': comentarios.paginator.num_pages,
                      }

        return render_to_response('usuarios/listar_comentarios.html', {'pagination' : pagination,
                                                                       'es_estacionamiento' : es_estac,
                                                                       'estacionamiento' : estacionamiento},
                                                                        context_instance=RequestContext(request))

    except Estacionamiento.DoesNotExist:
        raise Http404()

@user_passes_test(es_administrador, login_url='/users/login/')
def eliminar_comentario(request, id):
    """
    Vista para elimiar comentarios
    """
    try:
        comment = Comentarios.objects.get(pk=id)
        comment.delete()
    except Comentarios.DoesNotExist:
        raise Http404()
    return HttpResponseRedirect('/users/admin/listar_comentarios/%s/'%comment.estacionamiento_id)

@user_passes_test(es_administrador, login_url='/users/login/')
def listar_usuarios(request, page=1):
    """
    Vista para listar Clientes registrados
    """
    try:
        clientes = Cliente.objects.all()
        paginator = Paginator(clientes, 20)
        try:
            page = int(page)
        except:
            page = 1

        try:
            clientes = paginator.page(page)
        except (EmptyPage, InvalidPage):
            clientes = paginator.page(paginator.num_pages)

        pagination = {'object_list': [x.to_dict() for x in clientes.object_list],
                      'has_prev': clientes.has_previous(),
                      'has_next': clientes.has_next(),
                      'prev_page': clientes.previous_page_number() if clientes.has_previous() else None,
                      'next_page': clientes.next_page_number() if clientes.has_next() else None,
                      'page': clientes.number,
                      'num_pages': clientes.paginator.num_pages,
                      }
        return render_to_response('usuarios/listar_usuarios.html', {'pagination' : pagination}, context_instance=RequestContext(request))
    except Cliente.DoesNotExist:
        raise Http404()

@user_passes_test(es_administrador, login_url='/users/login/')
def eliminar_usuario(request, id):
    """
    Vista para hacer soft deletede clientes registrados
    """
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.activo = not cliente.activo
        cliente.save()
    except Cliente.DoesNotExist:
        raise Http404()
    return HttpResponseRedirect('/users/admin/listar_usuarios/')

@user_passes_test(es_estacionamiento, login_url='/users/login/')
def denunciar_comentario(request, id):
    """
    Vista para que el estacionamiento marque como spam a uncomentario
    """
    if 0==0:
        comment = Comentarios.objects.get(pk=id, estacionamiento=request.user.estacionamiento)
        comment.spam = not comment.spam
        comment.save()
    '''except Comentarios.DoesNotExist:
        raise Http404()'''
    return HttpResponseRedirect('/users/admin/listar_comentarios/%s/'%comment.estacionamiento_id)

def new_password(user):
    """
        Generador de passwords
    """
    new_pass = hashlib.sha512("%s12345"%user).hexdigest()
    return new_pass

def login(request):
    """
    Vista para loguear usuarios (estacionamientos y admin)
    """
    (admin, nuevo) = UsuarioBase.objects.get_or_create(nombre_usuario='admin')
    if True:
        admin.password = hashlib.sha512('adminclave').hexdigest()
        admin.administrador = True
        admin.save()

    errors = None
    if request.method == 'POST':
        if 'username' not in request.POST or 'password' not in request.POST:
            errors = 'Debe llenar todos los campos'
        else:
            try:
                user = UsuarioBase.objects.get(nombre_usuario = request.POST['username'],
                    password = hashlib.sha512(request.POST['password']).hexdigest())
            except:
                user = None
            if user is None or not user.activo:
                errors = u'Nombre de usuario o contraseña no coinciden'
            else:
                existe_estacionmiento = Estacionamiento.objects.all().filter(usuariobase_ptr_id=user.id).exists()
                if existe_estacionmiento or user.administrador:
                    user.login(request)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.GET['next'])
                    else:
                        if existe_estacionmiento:
                            return HttpResponseRedirect('/users/park/editar_estacionamiento/')
                        else:
                            return HttpResponseRedirect('/users/admin/listar_estacionamientos/')
                else:
                    errors = u'Nombre de usuario o contraseña no coinciden'

    return render_to_response('login.html', {'errors' : errors}, context_instance=RequestContext(request))

def logout(request):
    """
    Vista para desloguear usuario (cualquier tipo)
    """
    del request.session['SESSION_KEY']
    return HttpResponseRedirect("/")