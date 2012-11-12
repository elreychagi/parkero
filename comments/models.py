# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile, Parking

class Comment(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    spam = models.BooleanField(default=False, db_index=True)
    content = models.TextField(max_length=140)
    parking = models.ForeignKey(Parking)

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
        ordering =  ['-date']

class Points(models.Model):
    user = models.ForeignKey(UserProfile)
    date = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    parking = models.ForeignKey(Parking)

    class Meta:
        unique_together = ('user', 'parking')