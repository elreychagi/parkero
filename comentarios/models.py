# -*- coding: utf-8 -*-
from django.db import models
from usuarios.models import Cliente, Estacionamiento

class Comentarios(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    spam = models.BooleanField(default=False, db_index=True)
    contenido = models.TextField(max_length=140)
    estacionamiento = models.ForeignKey(Estacionamiento)

    def to_dict(self, admin=False, cliente=None):
        data = {'fecha' : self.fecha.strftime("%d/%m/%Y H:M"),
                'spam' : self.spam,
                'contenido' : self.contenido}
        if cliente:
            data.update({'cliente' : True if self.cliente.id == cliente.id else False,
                         'id' : self.id})
        if admin:
            data.update({'estacionamiento' : self.estacionamiento.to_dict(admin=True),
                         'id' : self.id,
                         'cliente' : self.cliente.to_dict()})

        return data

    class Meta:
        ordering =  ['-fecha']

class Puntos(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    puntos = models.IntegerField(default=0)
    estacionamiento = models.ForeignKey(Estacionamiento)

    class Meta:
        unique_together = ('cliente', 'estacionamiento')