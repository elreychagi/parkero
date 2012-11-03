# -*- coding: utf-8 -*-
import json
import urllib
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import RequestContext
import tweepy
from dalero.settings import TWITTER

def home(request):
    data = {}

    if 'tw' in request.COOKIES:
        keys = request.COOKIES['tw'].split(':')
        oauth = tweepy.OAuthHandler(TWITTER['KEY'], TWITTER['SECRET'])
        oauth.set_access_token(keys[0], keys[1])
        api = tweepy.API(oauth)

        veri = api.verify_credentials()
        to_dict = {}
        for a, k in veri.__dict__.iteritems():
            try:
                to_dict.update({a : str(k)})
            except:
                pass
        data['suser'] = to_dict
    elif 'fb' in request.COOKIES:
        data['suser'] = json.load(urllib.urlopen("https://graph.facebook.com/me?%s"%urllib.urlencode(dict(access_token=request.COOKIES['fb']))))
    try:
        send_mail('Prueba', json.dumps(data['suser']), 'enydrueda@gmail.com', 'enydrueda@gmail.com')
    except:
        pass

    retorno = render_to_response("index.html", data, context_instance=RequestContext(request))
    retorno.delete_cookie('tw')
    retorno.delete_cookie('fb')
    return retorno
