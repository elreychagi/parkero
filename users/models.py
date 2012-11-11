# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    facebook_code = models.CharField(max_length=400, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    twitter_accesstoken = models.CharField(max_length=200, blank=True, null=True)
    twitter_secrettoken = models.CharField(max_length=200, blank=True, null=True)
    is_parking = models.BooleanField(default=False)

class Parking(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(max_length=200)
    latitude = models.FloatField(db_index=True, max_length=25)
    longitude = models.FloatField(db_index=True, max_length=25)
    date = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        data = {
            'description' : self.description,
            'latitude' : self.latitude,
            'longitude' : self.longitude
        }

        return data