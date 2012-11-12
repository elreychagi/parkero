# -*- coding: utf-8 -*-
from django import forms

class FormParking(forms.Form):
    username = forms.RegexField(label = u'Nombre de usuario',
        regex=r'^[^\ ]+$',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder':'No se permiten espacios'}))

    nombre = forms.CharField(label='Nombre del estacionamiento',
        max_length=100,
        widget=forms.TextInput())

    email = forms.EmailField(label = u'Correo Electrónico',
        max_length=75,
        widget= forms.TextInput())

    description = forms.CharField(label = u'Descripción',
        max_length=200,
        widget= forms.Textarea())

    latitude = forms.DecimalField(label = u'Latitude',
        max_digits= 17,
        decimal_places=15,
        widget= forms.TextInput(attrs={'placeholder':'12.123456789012345'}))

    longitude = forms.DecimalField(label = u'Longitude',
        max_digits= 17,
        decimal_places=15,
        widget= forms.TextInput(attrs={'placeholder':'12.123456789012345'}))

    parking = forms.IntegerField(required=True, widget=forms.HiddenInput())

    def __init__(self, edit=False, *args, **kwargs):
        super(FormParking, self).__init__(*args, **kwargs)
        if not edit:
            del self.fields['parking']
        else:
            self.fields['username'].widget = forms.TextInput(attrs={'readonly':'true'})