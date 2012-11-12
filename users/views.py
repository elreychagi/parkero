# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import json
import random
from subprocess import Popen, PIPE
import urllib
import urlparse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import tweepy
from comments.models import Comment
from dalero.settings import TWITTER, FACEBOOK, SECRET_KEY
from users.forms import FormParking
from users.models import UserProfile, Parking
from users.permisos import *

def twitter_connect(request):
    """
        Inicio del proceso oauth de Twitter
        Se obtiene el request_token para luego redireccionar al usuario a la página para solicitar permiso de acceso
    """

    try:
        auth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'], TWITTER["CALLBACK"])
        redirect_url = auth.get_authorization_url()
        rkey = auth.request_token.key
        rsecret = auth.request_token.secret

        tw_rt = "%s::%s"%(rkey, rsecret)
        response = HttpResponseRedirect(redirect_url)
        response.set_signed_cookie("tw_rt", tw_rt, salt=SECRET_KEY)
        return response
    except:
        pass
    return HttpResponseRedirect('/?error_twitter')

def twitter_callback(request):
    """
        Una vez el usuario permise o no el acceso a su cuenta de Twitter esta vista revisa si concedio permisos o no
        En caso afirmativo busca a un usuario con ese id de Twitter para crear la sesion, de no existir crea al usuario
    """
    retorno = HttpResponseRedirect('/')
    if 0==0:
        s = request.get_signed_cookie("tw_rt", salt=SECRET_KEY)
        tokens = s.split('::')
        request_token = tokens[0]
        request_secret = tokens[0]
        if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
            oauth_token = request.GET['oauth_token']
            oauth_verifier = request.GET['oauth_verifier']

            oauth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'])
            oauth.set_request_token(request_token, request_secret)
            oauth.get_access_token(oauth_verifier)

            api = tweepy.API(oauth)
            tw_user = api.verify_credentials()
            try:
                user_p = UserProfile.objects.get(twitter_id=tw_user.id)
                user_p.user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user_p.user)
            except UserProfile.DoesNotExist:
                accesstoken = oauth.access_token.key
                secret = oauth.access_token.secret
                user = User.objects.create_user(username="%s_tc"%tw_user.screen_name)
                user.is_active = True
                user.first_name = tw_user.name
                user.save()
                user_p = UserProfile(user=user,
                                    twitter_id=tw_user.id,
                                    twitter_accesstoken=accesstoken,
                                    twitter_secrettoken=secret)
                user_p.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
            retorno = HttpResponseRedirect('/app/')
    '''except:
        retorno = HttpResponseRedirect('/?error_twitter')'''
    #retorno.delete_cookie("tw_rt")
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
    try:
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
                        user_p = UserProfile.objects.get(facebook_id=fb_user['id'])
                        user_p.user.backend = 'django.contrib.auth.backends.ModelBackend'
                        auth.login(request, user_p.user)
                    except UserProfile.DoesNotExist:
                        user = User.objects.create_user(username="%s_fb"%fb_user['username'])
                        user.is_active = True
                        user.first_name = fb_user['first_name']
                        user.last_name = fb_user['last_name']
                        user.save()

                        user_p = UserProfile(user=user,
                            facebook_id=fb_user['id'],
                            facebook_accesstoken=access_token,
                            facebook_code=code)
                        user_p.save()
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        auth.login(request, user)
                    retorno = HttpResponseRedirect('/app/')
    except:
        pass
    return retorno

@user_passes_test(admin_user, login_url='/users/login/')
def new_parking(request):
    errors = {}
    if request.method != 'POST':
        form = FormParking()
    else:
        form = FormParking(data=request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data

            if User.objects.all().filter(username=clean_data['username']).count() > 0:
                errors = {'username' : {'as_text':'* Nombre de usuario usado'}}
            elif User.objects.all().filter(email=clean_data['email']).count() > 0:
                errors = {'email' : {'as_text':'* Correo electrónico usado'}}
            else:
                password = new_password()
                user = User.objects.create_user(username=clean_data['username'],
                                                email=clean_data['email'],
                                                password=password)
                user.save()

                parking = Parking(user=user,
                                description=clean_data['description'],
                                nombre=clean_data['nombre'],
                                latitude=clean_data['latitude'],
                                longitude=clean_data['longitude'])
                parking.save()

            msg = MIMEText(u"Bienvenido a Dalero.net su contraseña de ingreso es %s"%password,'html')
            msg["From"] = "enydrueda@gmail.com"
            msg["To"] = user.email
            msg["Subject"] = "Bienvenido a Dalero.net"
            p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
            p.communicate(msg)
            return HttpResponseRedirect('/users/admin/listar_estacionamientos/')
        else:
            errors = form.errors
    return render_to_response('admin/admin_parkings.html', {'form' : form, 'errors' : errors}, context_instance=RequestContext(request))

@user_passes_test(admin_user, login_url='/users/login/')
def list_parkings(request, page=1):
    parkings = [x.to_dict(admin=True) for x in Parking.objects.all().filter(user__is_active=True)]

    paginator = Paginator(parkings, 20)
    
    try:
        page = int(page)
    except:
        page = 1

    try:
        parkings = paginator.page(page)
    except (EmptyPage, InvalidPage):
        parkings = paginator.page(paginator.num_pages)

    next_page = parkings.next_page_number() if parkings.has_next() else 0

    pagination = {'object_list': parkings.object_list,
                          'has_prev': parkings.has_previous(),
                          'has_next': parkings.has_next(),
                          'prev_page': parkings.previous_page_number() if parkings.has_previous() else None,
                          'next_page': next_page if parkings.has_next() else None,
                          'page': parkings.number,
                          'num_pages': parkings.paginator.num_pages,
    }
    
    return render_to_response('admin/list_parkings.html', {'pagination' : pagination,}, context_instance=RequestContext(request))

@user_passes_test(admin_user, login_url='/users/login/')
def edit_parking(request, id):
    errors = {}
    try:
        parking = Parking.objects.get(pk=id)
        if request.method != 'POST':
            form = FormParking(initial={'nombre' : parking.nombre,
                                        'username' : parking.user.username,
                                        'email' : parking.user.email,
                                        'description' : parking.description,
                                        'latitude' : parking.latitude,
                                        'longitude' : parking.longitude,
                                        'parking' : parking.id},
                                        edit=True)
        else:
            form = FormParking(data=request.POST, edit=True)
            if form.is_valid():
                clean_data = form.cleaned_data
                if User.objects.all().exclude(pk=parking.user.pk).filter(email=clean_data['email']).count() > 0:
                    errors = {'email' : {'as_text':'* Correo electrónico usado'}}
                else:
                    user = parking.user
                    user.email = clean_data['email']
                    user.save()

                    parking.description = clean_data['description']
                    parking.nombre = clean_data['nombre']
                    parking.latitude = clean_data['latitude']
                    parking.longitude = clean_data['longitude']
                    parking.save()
            else:
                errors = form.errors
        return render_to_response('admin/admin_parkings.html', {'form' : form, 'errors' : errors}, context_instance=RequestContext(request))
    except Parking.DoesNotExist:
        raise Http404()

@user_passes_test(admin_user, login_url='/users/login/')
def delete_parking(request, id):
    try:
        parking = Parking.objects.get(pk=id)
        parking.user.is_active = not parking.user.is_active
        parking.user.save()
        return HttpResponseRedirect('/users/admin/listar_estacionamientos/')
    except Parking.DoesNotExist:
        raise Http404()

@user_passes_test(admin_user, login_url='/users/login/')
def list_comments(request, park, page=1):
    try:
        parking = Parking.objects.get(pk=park, user__is_active=True)
        comments = [x.to_dict(admin=True) for x in Comment.objects.all().filter(parking__id=parking.id, userprofile__user__is_active=True)]

        paginator = Paginator(comments, 20)

        try:
            page = int(page)
        except:
            page = 1

        try:
            parkings = paginator.page(page)
        except (EmptyPage, InvalidPage):
            parkings = paginator.page(paginator.num_pages)

        next_page = parkings.next_page_number() if parkings.has_next() else 0

        pagination = {'object_list': parkings.object_list,
                      'has_prev': parkings.has_previous(),
                      'has_next': parkings.has_next(),
                      'prev_page': parkings.previous_page_number() if parkings.has_previous() else None,
                      'next_page': next_page if parkings.has_next() else None,
                      'page': parkings.number,
                      'num_pages': parkings.paginator.num_pages,
                      }

        return render_to_response('admin/list_comments.html', {'pagination' : pagination, 'parking' : park}, context_instance=RequestContext(request))
    except Parking.DoesNotExist:
        raise Http404()

@user_passes_test(admin_user, login_url='/users/login/')
def delete_comments(request, parking, id):
    try:
        comment = Comment.objects.get(pk=id)
        comment.delete()
    except Parking.DoesNotExist:
        raise Http404()
    except:
        pass
    return HttpResponseRedirect('/users/admin/listar_comentarios/%s/'%parking)

@user_passes_test(admin_user, login_url='/users/login/')
def list_users(request, page=1):
    try:
        users = [x.to_dict() for x in UserProfile.objects.all()]

        paginator = Paginator(users, 20)

        try:
            page = int(page)
        except:
            page = 1

        try:
            parkings = paginator.page(page)
        except (EmptyPage, InvalidPage):
            parkings = paginator.page(paginator.num_pages)

        next_page = parkings.next_page_number() if parkings.has_next() else 0

        pagination = {'object_list': parkings.object_list,
                      'has_prev': parkings.has_previous(),
                      'has_next': parkings.has_next(),
                      'prev_page': parkings.previous_page_number() if parkings.has_previous() else None,
                      'next_page': next_page if parkings.has_next() else None,
                      'page': parkings.number,
                      'num_pages': parkings.paginator.num_pages,
                      }

        return render_to_response('admin/list_users.html', {'pagination' : pagination}, context_instance=RequestContext(request))
    except UserProfile.DoesNotExist:
        raise Http404()

@user_passes_test(admin_user, login_url='/users/login/')
def delete_user(request, id):
    try:
        user = UserProfile.objects.get(pk=id)
        user.user.is_active = not user.user.is_active
        user.user.save()
    except Parking.DoesNotExist:
        raise Http404()
    except:
        pass
    return HttpResponseRedirect('/users/admin/listar_usuarios/')

def new_password():
    """
        Generador de passwords
    """
    pass_caracteres = "123456789ABCDEFGHIJKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed()
    new_pass = ""
    for i in range(0, 10):
        new_pass = new_pass + pass_caracteres[random.randrange(0, len(pass_caracteres))]
    password = new_pass
    return password

def login(request):
    errors = None
    if request.method == 'POST':
        if 'username' not in request.POST or 'password' != request.POST:
            errors = 'Debe llenar todos los campos'

        user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])

        if user is None or not user.is_active or hasattr(user, 'userprofile'):
            errors = u'Nombre de usuario o contraseña no coinciden'
        else:
            auth.login(request, user)

            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                if hasattr(user, 'parking'):
                    return HttpResponseRedirect('/users/parking/')
                if user.is_superuser:
                    return HttpResponseRedirect('/users/admin/listar_estacionamientos/')


    return render_to_response('login.html', {'errors' : errors}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")