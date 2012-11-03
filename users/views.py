# -*- coding: utf-8 -*-
import json
import urllib
import urlparse
from django.contrib.sessions.backends.file import SessionStore
from django.http import HttpResponseRedirect, HttpResponse
import tweepy
from dalero.settings import TWITTER, FACEBOOK

def twitter_connect(request):
    """
        Inicio del proceso oauth de Twitter
        Se obtiene el request_token para luego redireccionar al usuario a la página para solicitar permiso de acceso
    """

    s = SessionStore()
    try:
        auth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'], TWITTER["CALLBACK"])
        redirect_url = auth.get_authorization_url()
        rkey = auth.request_token.key
        rsecret = auth.request_token.secret

        tw_rt = "%s::%s"%(rkey, rsecret)
        s['tw_rt'] = tw_rt
        s.save()
        response = HttpResponseRedirect(redirect_url)
        response.set_cookie("tw_rt", tw_rt)
        return response
    except:
        pass
    return HttpResponse("Error inesperado")

def twitter_callback(request):
    """
        Una vez el usuario permise o no el acceso a su cuenta de Twitter esta vista revisa si concedio permisos o no
        En caso afirmativo busca a un usuario con ese id de Twitter para crear la sesion, de no existir crea al usuario
    """
    if "denied" in request.GET:
        return HttpResponse("access denied")
    retorno = HttpResponseRedirect('/')
    if 'tw_rt' in request.COOKIES:
        s = request.COOKIES["tw_rt"]
        if s is not None:
            tokens = s.split('::')
            request_token = tokens[0]
            request_secret = tokens[0]
            if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
                oauth_token = request.GET['oauth_token']
                oauth_verifier = request.GET['oauth_verifier']

                oauth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'])
                oauth.set_request_token(request_token, request_secret)
                oauth.get_access_token(oauth_verifier)

                key = oauth.access_token.key
                secret = oauth.access_token.secret

                retorno.set_cookie('tw', '%s:%s'%(key,secret))
    retorno.delete_cookie("tw_rt")
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
    retorno = HttpResponseRedirect('/')
    if code is not None:
        args = dict(client_id=FACEBOOK["KEY"], redirect_uri=FACEBOOK["CALLBACK"], client_secret=FACEBOOK["SECRET"], code=code)
        response = urlparse.parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?%s"%urllib.urlencode(args)).read())

        access_token = response["access_token"][-1]

        if access_token is not None:
            retorno.set_cookie('fb', access_token)
    return retorno