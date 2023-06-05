from django.db import models
from django.core.exceptions import ValidationError
import re

#Email validation:
#Eiqui o que se fai é comprobar se o e-mail está na lista negra dos dominios. Básicamente o que trato de facer e que non me metan correos spam
def email_validation_black_list(self):
    with open("NovaEra/static/disposable_email_doamins.txt", "r") as file_spam_emails:
        #O splitlines é para convertilo a unha lista
        blacklist = file_spam_emails.read().splitlines()
        #Miramos se todo o que está despois do @ está contida na lista negra dos e-mails
        correo_ben=re.search(r"([a-zA-Z0-9äüö_.+-]+$)", self)
        if correo_ben[1] in blacklist:
            raise ValidationError("O teu e-mail é un correo Spam. Por favor, inténteo con outro email")
        else:
             return self

# def email_validation_correct_format(self):
#     correo=re.search(r"pepe@gmail.com", self)
#     return correo[1]

# Create your models here.
class newsletter_email(models.Model):
    email_subscriptor = models.EmailField(blank=False, max_length=255, validators=[email_validation_black_list])

    def __str__(self):
        return (self.email_subscriptor)  
