# -*- coding: utf-8 -*-
from django import forms

class FormEstacionamiento(forms.Form):
    nombre_usuario = forms.RegexField(label = u'Nombre de usuario',
        regex=r'^[^\ ]+$',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder':'No se permiten espacios'}))

    nombre = forms.CharField(label='Nombre del estacionamiento',
        max_length=100,
        widget=forms.TextInput())

    correo = forms.EmailField(label = u'Correo Electrónico',
        max_length=75,
        widget= forms.TextInput(attrs={'placeholder':u'Correo electrónico válido'}))

    descripcion = forms.CharField(label = u'Descripción',
        max_length=200,
        widget= forms.Textarea())

    latitud = forms.DecimalField(label = u'Latitude',
        max_digits= 17,
        decimal_places=15,
        widget= forms.TextInput(attrs={'placeholder':'12.123456789012345'}))

    longitud = forms.DecimalField(label = u'Longitude',
        max_digits= 17,
        decimal_places=15,
        widget= forms.TextInput(attrs={'placeholder':'12.123456789012345'}))

    motos = forms.BooleanField(label='Aceptan motos',
        required= False,
        widget= forms.CheckboxInput())

    camiones = forms.BooleanField(label='Aceptan camiones',
        required= False,
        widget= forms.CheckboxInput())

    sin_techo = forms.BooleanField(label='Sin techo',
        required= False,
        widget= forms.CheckboxInput())

    id = forms.IntegerField(required=True, widget=forms.HiddenInput())

    def __init__(self, edit=False, parking=False, *args, **kwargs):
        super(FormEstacionamiento, self).__init__(*args, **kwargs)
        if not edit:
            del self.fields['id']
        else:
            self.fields['nombre_usuario'].widget = forms.TextInput(attrs={'readonly':'true'})
            if parking:
                del self.fields['latitud']
                del self.fields['longitud']