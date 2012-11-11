# -*- coding: utf-8 -*-
import json
import urllib
import urlparse
from django.contrib import auth
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
import tweepy
from dalero.settings import TWITTER, FACEBOOK, SECRET_KEY
from users.models import UserProfile, Parking

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

def list_points(request):
    lat = float(request.GET['lat'])
    long = float(request.GET['long'])
    radius = 1
    distance_unit = 6371

    cursor = connection.cursor()

    sql = """SELECT id, latitude, longitude FROM users_parking WHERE (%f * acos( cos( radians(%f) ) * cos( radians( latitude ) ) *
        cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitude ) ) ) ) < %d
        """ % (distance_unit, lat, long, lat, int(radius))
    cursor.execute(sql)
    ids = [row[0] for row in cursor.fetchall()]

    parkings =[x.to_dict() for x in Parking.objects.all().filter(id__in=ids)]
    return HttpResponse(json.dumps({'success' : True, 'parkings' : parkings}), mimetype='application/json')