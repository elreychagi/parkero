# -*- coding: utf-8 -*-
from django.db import models
from usuarios.models import Cliente

class PosicionCliente(models.Model):
    cliente = models.ForeignKey(Cliente)
    latitud = models.FloatField(db_index=True, max_length=25)
    longitud = models.FloatField(db_index=True, max_length=25)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    primero = models.BooleanField(default=True)