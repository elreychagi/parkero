# -*- coding: utf-8 -*-
from django.db import connection
from django.http import HttpResponse
from tweepy.streaming import json
from users.models import Parking


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

    parkings =[x.to_dict() for x in Parking.objects.all().filter(id__in=ids, user__is_active=True)]
    return HttpResponse(json.dumps({'success' : True, 'parkings' : parkings}), mimetype='application/json')
