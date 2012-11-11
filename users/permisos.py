# -*- coding: utf-8 -*-
from functools import wraps
import json
import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.utils.decorators import available_attrs
from dalero import settings

def social_user(user):
    return user.is_authenticated() and (user.userprofile.facebook_id != None or user.userprofile.twitter_id != None)

def user_passes_test(test_func, login_url=None, login_json=False, redirect_field_name=REDIRECT_FIELD_NAME):

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()

            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                           settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            if login_json:
                return HttpResponse(json.dumps({'success':False,'cause':'403'}))
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator