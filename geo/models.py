# -*- coding: utf-8 -*-
from django.db import models
from users.models import Cliente

class PosicionCliente(models.Model):
    cliente = models.ForeignKey(Cliente)
    latitud = models.FloatField(db_index=True, max_length=25)
    longitud = models.FloatField(db_index=True, max_length=25)
    fecha = models.DateTimeField(auto_created=True)
    primero = models.BooleanField(default=True)