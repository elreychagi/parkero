# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.db.models import Avg

class Permisos(models.Model):
    pass

class UsuarioBase(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    creacion = models.DateTimeField(auto_created=True)
    ultimo_acceso = models.DateTimeField(auto_now_add=True)

class IntentosIngreso(models.Model):
    ip = models.IPAddressField(blank=False, null=False, db_index=True)
    fecha = models.DateTimeField(auto_created=True)

class Cliente(UsuarioBase):
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    facebook_code = models.CharField(max_length=400, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    twitter_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    twitter_secrettoken = models.CharField(max_length=200, blank=True, null=True)

    def to_dict(self):
        data = {'username' : self.user.username,
                'facebook' : self.facebook_id is not None,
                'id' : self.id,
                'active' : self.user.is_active,
                'twitter' : self.twitter_id is not None}
        return data

class Estacionamiento(UsuarioBase):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200)
    latitud = models.FloatField(db_index=True, max_length=25)
    longitud = models.FloatField(db_index=True, max_length=25)
    fecha_creacion = models.DateTimeField(auto_created=True)
    motos = models.BooleanField(default=False)
    camiones = models.BooleanField(default=False)
    sin_techo = models.BooleanField(default=False)

    def to_dict(self, admin=False):
        points = self.points_set.all().aggregate(Avg('points'))['points__avg']
        data = {
            'name' : self.name,
            'description' : self.description,
            'latitude' : str(self.latitude),
            'longitude' : str(self.longitude),
            'points' : '%s de 10'%(int(round(points, 2)) if points is not None else 0.0),
            'motorbikes' : self.motorbikes,
            'truks' : self.truks,
            'open' : self.open,
            'comments' : self.comment_set.all().count()
        }

        if admin:
            data.update({'email' : self.user.email,
                         'id' : self.id,
                         'active' : self.user.is_active})

        return data