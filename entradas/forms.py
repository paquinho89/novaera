from django import forms
from django.forms import ModelForm
from entradas.models import entradas_modelo


class entradas_reserva_form(forms.ModelForm):
    class Meta:
        model=entradas_modelo
        fields = ['nome', 'apelidos', 'correo_electrónico_entradas', 'numero_entradas']
#Esto dos widgets é para meter o formato de bootstrap no form. {{ form }} que está en artigos_content.html.
#O attrs é CSS style
        widgets = {
            'nome': forms.TextInput (attrs = {'class': 'form-control'}),
            'apelidos': forms.TextInput (attrs = {'class': 'form-control'}),
            'correo_electrónico_entradas': forms.TextInput (attrs = {'class': 'form-control'}),
            'numero_entradas': forms.Select (attrs = {'class': 'form-control'})
        }