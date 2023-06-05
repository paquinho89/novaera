from logging.config import IDENTIFIER
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput

# Create your models here.
entradas_choices = [(i,i) for i in range(1,4)]

# Create your models here.
class entradas_modelo(models.Model):
    nome = models.CharField(blank=False, max_length=255)
    apelidos = models.CharField(blank=False, max_length=255)
    #ESTO PÓDECHE SER MUI ÚTIL PARA A PÁXINA DAS CARREIRAS DE ULTRACYCLING
    #O unique do correo electrónico é para que unha mesma persona non poda facer 2 reservas, e se a intenta facer sale o erro que se describe a continuación.
    #correo_electrónico_entradas = models.EmailField(primary_key=True, blank=False, max_length=255, error_messages={'unique':"Este correo xa se usuo para facer a reserva"})
    correo_electrónico_entradas = models.EmailField(max_length=255)
    numero_entradas = models.IntegerField(blank=False, null=False, choices=entradas_choices)
    data_rexistro = models.DateTimeField (default=datetime.now, blank=True)




