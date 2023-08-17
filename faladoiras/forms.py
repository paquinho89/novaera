from django import forms
from django.forms import ModelForm
from faladoiras.models import faladoiras_comments


class CommentForm(forms.ModelForm):
    class Meta:
        model=faladoiras_comments
        fields = ['nome', 'correo_electrónico', 'comentario']
#Esto dos widgets é para meter o formato de bootstrap no form. {{ form }} que está en artigos_content.html.
#O attrs é CSS style
        widgets = {
            'nome': forms.TextInput (attrs = {'class': 'form-control'}),
            'correo_electrónico': forms.TextInput (attrs = {'class': 'form-control'}),
            'comentario': forms.Textarea (attrs = {'class': 'form-control'})
        }


