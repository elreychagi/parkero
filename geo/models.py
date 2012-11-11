# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile

class UserPosition(models.Model):
    user = models.ForeignKey(UserProfile)
    latitude = models.FloatField(db_index=True, max_length=25)
    longitude = models.FloatField(db_index=True, max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    first = models.BooleanField(default=True)