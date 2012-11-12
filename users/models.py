# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Avg

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    facebook_code = models.CharField(max_length=400, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    twitter_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    twitter_secrettoken = models.CharField(max_length=200, blank=True, null=True)

    def to_dict(self):
        data = {'username' : self.user.username,
                'facebook' : self.facebook_id is not None,
                'twitter' : self.twitter_id is not None}
        return data

class Parking(models.Model):
    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    latitude = models.FloatField(db_index=True, max_length=25)
    longitude = models.FloatField(db_index=True, max_length=25)
    date = models.DateTimeField(auto_now_add=True)

    def to_dict(self, admin=False):
        points = self.points_set.all().aggregate(Avg('points'))['points__avg']
        data = {
            'nombre' : self.nombre,
            'description' : self.description,
            'latitude' : str(self.latitude),
            'longitude' : str(self.longitude),
            'points' : '%s de 10'%(int(round(points, 2)) if points is not None else 0.0),
            'comments' : self.comment_set.all().count()
        }

        if admin:
            data.update({'email' : self.user.email,
                         'id' : self.id,
                         'active' : self.user.is_active})

        return data