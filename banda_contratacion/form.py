import email
from unittest.util import _MAX_LENGTH
from webbrowser import open_new
from django import forms
from django.forms import ModelForm
from .models import contratacion_datos



class contratacionForm(forms.ModelForm):
    class Meta:
        model=contratacion_datos
        fields = ( 'toda_banda', 'cuarteto', 'terceto_opcion_1', 'terceto_opcion_2', 'duo_opcion_1', 'duo_opcion_2', 'conxunto', 'tipo_evento', 'data_evento', 
                    'lugar_evento', 'nome', 'teléfono', 'correo_electrónico', 'mais_info' )
        widgets = {
            'toda_banda': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'cuarteto': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'terceto_opcion_1': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'terceto_opcion_2': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'duo_opcion_1': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'duo_opcion_2': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'conxunto': forms.CheckboxInput (attrs = {'style':'width:25px; height:25px;'}),
            'tipo_evento': forms.Select (attrs = {'class': 'form-control'}),
            'data_evento': forms.DateInput (attrs= {'class': 'form-control'}),
            'lugar_evento': forms.TextInput (attrs = {'class': 'form-control', 'placeholder':'Ex: "Soutochao"'}),
            'nome': forms.TextInput (attrs = {'class': 'form-control', 'placeholder':'Ex: "Pepa"'}),
            'teléfono': forms.TextInput (attrs = {'class': 'form-control', 'placeholder':'Ex: "666777888"'}),
            'correo_electrónico': forms.EmailInput (attrs = {'class': 'form-control', 'placeholder':'Ex: "pepa@gmail.com"'}),
            'mais_info': forms.Textarea (attrs = {'class': 'form-control'})
        }

        