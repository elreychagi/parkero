# -*- coding: utf-8 -*-
from django.db import models
from users.models import Cliente, Estacionamiento

class Comment(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_created=True, db_index=True)
    spam = models.BooleanField(default=False, db_index=True)
    contenido = models.TextField(max_length=140)
    estacionamiento = models.ForeignKey(Estacionamiento)

    def to_dict(self, admin=False):
        data = {'date' : self.date.strftime("%d/%m/%Y H:M"),
                'content' : self.content}

        if admin:
            data.update({'parking' : self.parking.to_dict(admin=True),
                         'id' : self.id,
                         'userprofile' : self.userprofile.to_dict()})
        else:
            data.update({'parking' : self.parking.to_dict()})

        return data

    class Meta:
        ordering =  ['-fecha']

class Puntos(models.Model):
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_created=True)
    puntos = models.IntegerField(default=0)
    estacionamiento = models.ForeignKey(Estacionamiento)

    class Meta:
        unique_together = ('cliente', 'estacionamiento')