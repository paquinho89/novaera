from pickle import FALSE
from pyexpat import model
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
import re

# Create your models here.
evento_choices = (
    ('festival','Festival'),
    ('festa_aldea', 'Festa aldea'),
    ('voda', 'Voda'),
    ('bautizo', 'Bautizo'),
    ('aniversario', 'Aniversario'),
    ('funeral', 'Funeral'),
    ('outros', 'Outros')
)

#Phone number_validation:
#Eiqui o que se fai é comprobar se o número de teléfono ten 9 ou máis de 9 caracteres.
def telephone_number_validation(self):
    if len(str(self))>=9:
        return self
    else:
        raise ValidationError("Insira un número de teléfono con 9 díxitos ou maís")

#SEGUE POR EIQUI. TES QUE APLICARLLE OS VALIDATORS AO CONXUNTO
#Conxunto validation:
#Creo unha lista vacía para ir metendo (append) os True/False dos valores dos check Box.
#Este validator aplica a todos os atributos do modelo, xa que teño que coller o True ou False de cada check Box.
lista_booleana=[]
def conxunto_validation(self):
    lista_booleana.append(self)
#Eiqui unha vez que teño todos os True/False metidos na lista, comprobo se hai ao menos un True. Este validatos olo afecta ao último atributo do modelo xa que
#quero que se execute unha soa vez
def enviar_mensaxe_error(self):
    #print('pepe')
    #print(any(lista_booleana))
    #"Any" devólveme un valor True se na lista hai ao menos un True. Se todos os valores son False, pois devolve un False.
    if any(lista_booleana)==False:
        raise ValidationError("Por favor, seleccione ao menos un conxunto que estaría interesada/o en contratar")
    else:
        return self
#Eiqui elimino os valores da lista_booleana para que cando outro usuario cubra os datos, a lista esté vacía.
def limpiar_lista(self):
    #print(lista_booleana)
    lista_booleana.clear()
#----------------------------------------------------------------------------------------------------------------------
#Email validation para a xente que nos contrata:
#Eiqui o que se fai é comprobar se o e-mail está na lista negra dos dominios. Básicamente o que trato de facer e que non me metan correos spam
def email_validation_contratacion(self):
    with open("NovaEra/static/disposable_email_doamins.txt", "r") as file_spam_emails:
        #O splitlines é para convertilo a unha lista
        blacklist = file_spam_emails.read().splitlines()
        #Miramos se todo o que está despois do @ está contida na lista negra dos e-mails
        correo_ben=re.search(r"([a-zA-Z0-9äüö_.+-]+$)", self)
        if correo_ben[1] in blacklist:
            raise ValidationError("O teu e-mail é un correo Spam. Por favor, inténteo con outro email")
        else:
             return self

class contratacion_datos(models.Model):
    toda_banda = models.BooleanField('toda_banda', default=True, validators=[conxunto_validation])
    cuarteto = models.BooleanField('cuarteto', default=False, validators=[conxunto_validation])
    terceto_opcion_1 = models.BooleanField('terceto_opcion_1', default=False, validators=[conxunto_validation])
    terceto_opcion_2 = models.BooleanField('terceto_opcion_2', default=False, validators=[conxunto_validation])
    duo_opcion_1 = models.BooleanField('duo_opcion_1', default=False, validators=[conxunto_validation])
    duo_opcion_2 = models.BooleanField('duo_opcion_2', default=False, validators=[conxunto_validation])
    #Este é o campo Solista, pero póñolle "Advertencia" para que cando se me imprima a mensaxe de error, pois senon pondría Solista.
    conxunto = models.BooleanField('solista', default=False, validators=[conxunto_validation, enviar_mensaxe_error, limpiar_lista])
    tipo_evento = models.CharField(max_length=11, choices=evento_choices)
    data_evento = models.DateField (blank=False)
    lugar_evento = models.CharField(blank=False, max_length=255)
    nome = models.CharField(blank=False, max_length=255)
    teléfono = models.IntegerField(validators=[telephone_number_validation])
    correo_electrónico = models.EmailField(blank=False, max_length=255, validators=[email_validation_contratacion])
    mais_info = models.TextField(blank=True)
    #Teño que utilizar DateField e non podo utilizar o DateTimeField porque na base de datos de Postgress
    #de Railway non me acepta o datetime field.
    data_rexistro = models.DateField (default=datetime.now, blank=True, null=True)
    #data_rexistro = models.DateTimeField (default=datetime.now, blank=True)
    contestado = models.BooleanField('contestado', default=False)
    

    #A configuración do panel de administracion para banda_contratacon está no admin.py file
    
            
