# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.db.models import Avg

class UsuarioBase(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=128, null=True, blank=True)
    creacion = models.DateTimeField(auto_now=False, auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True, auto_now_add=True)
    administrador = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    correo = models.EmailField(null=True, blank=True)

    def login(self, request):
        request.session['SESSION_KEY'] = self.id
        self.save()
        return True

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
        data = {'nombre_usuario' : self.nombre_usuario,
                'facebook' : self.facebook_id is not None,
                'id' : self.id,
                'activo' : self.activo,
                'twitter' : self.twitter_id is not None}
        return data

class Estacionamiento(UsuarioBase):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200)
    latitud = models.FloatField(db_index=True, max_length=25)
    longitud = models.FloatField(db_index=True, max_length=25)
    motos = models.BooleanField(default=False)
    camiones = models.BooleanField(default=False)
    sin_techo = models.BooleanField(default=False)

    def to_dict(self, admin=False):
        puntos = self.puntos_set.all().aggregate(Avg('puntos'))['puntos__avg']
        data = {
            'nombre' : self.nombre,
            'descripcion' : self.descripcion,
            'latitud' : str(self.latitud),
            'longitud' : str(self.longitud),
            'puntos' : int(round(puntos, 2)) if puntos is not None else 0,
            'motos' : self.motos,
            'camiones' : self.camiones,
            'sin_techo' : self.sin_techo,
            'id' : self.id,
            'comentarios' : self.comentarios_set.all().count()
        }
        if admin:
            data.update({'correo' : self.correo,
                         'nombre_usuario' : self.nombre_usuario,
                         'activo' : self.activo})

        return data