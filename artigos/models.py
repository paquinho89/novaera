from email.policy import default
from logging import PlaceHolder
from django.db import models
from datetime import datetime, timezone
from django.utils.text import slugify
import os
from django.utils import timezone

from django.forms import DateField, DateInput
#Importo o slug random generator para que me meta o título do artigo no slug
from .helpers import unique_slug_generator
#Pero eu quero que o unique_slug_generator funcione antes de que o modelo (quero dicir,os datos) son gardados.
#E dicir, antes de que os datos sexan gardados ten que cubrir o slug
from django.db.models.signals import pre_save

from django.core.exceptions import ValidationError
import re
#PAra o rich text do text field dos artigos no django/admin
from ckeditor.fields import RichTextField

#Estas 2 funcions son para cambiarlle o nome e que aparezca guay no model do admin con outro nome

def get_filename_extension (filepath):
    #Esto colle a parte final da ruta, que será algo como "C/Users/Desktop/hat.png"
    #Pois o os.path.basename o que está facendo e colloer solo o "hat.png"
    base_name=os.path.basename(filepath)
    #Esto dividi o "hat.png" en hat (que será o name) e na ext (extensión), que será "png"
    name, ext =os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext= get_filename_extension(filename)
    # Generate a unique slug to avoid overwriting existing files
    slug = slugify(name)
    final_filename='{slug}{ext}'.format(slug=slug, ext=ext)
    return "static/static/media_files/{final_filename}".format(final_filename=final_filename)


# Create your models here.
class autores(models.Model):
    image_autor = models.ImageField(upload_to=upload_image_path, null=True, blank = True)
    name_autor = models.CharField(max_length=120, null=True, blank = True)
    description_autor = models.TextField()
    social_media = models.CharField(max_length=120, null=True, blank = True)

    def __str__(self):
        return self.name_autor

class artigos(models.Model):
    #O null=True é para que acepte valores en blano no data base e o blank=True é para que o valor non sexa requerido por Django, desta forma non fai falta que exista unha imaxe
    image = models.ImageField(upload_to=upload_image_path, null=True, blank = True)
    # Id = pk (Primary Key)
    #id = models.Field(primary_key = True)
    artigos_title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True, verbose_name="Deixar_en_blanco")
    artigos_summary = models.TextField()
    #artigos_content = models.TextField()
    artigos_content = RichTextField()
    author = models.ForeignKey(autores, related_name="artigos", on_delete=models.CASCADE, default=1)
    #Teño que utilizar DateField e non podo utilizar o DateTimeField porque na base de datos de Postgress
    #de Railway non me acepta o datetime field.
    artigos_date = models.DateField (default=datetime.now, blank=True, null=True)
    
    #Esto é para que me ordene os artigos por data
    class Meta:
        ordering = ['-artigos_date']

    #Está función e para que me cree a url específica para cada blog.
    def get_absolute_url(self):
        return "/artigos/{slug}/".format(slug=self.slug)    

    #Esto é para que no admin me colla o título do artículo e mo mostre no django admin
    #__str__ representa a clase dun obxeto (neste caso artigos_title) comounha cadena de texto. É como facer un print() ou un str()
    def __str__(self):
        return self.artigos_title

#Email validation:
#Eiqui o que se fai é comprobar se o e-mail está na lista negra dos dominios. Básicamente o que trato de facer e que non me metan correos spam
def email_validation(self):
    with open("NovaEra/static/disposable_email_doamins.txt", "r") as file_spam_emails:
        #O splitlines é para convertilo a unha lista
        blacklist = file_spam_emails.read().splitlines()
        #Miramos se todo o que está despois do @ está contida na lista negra dos e-mails
        correo_ben=re.search(r"([a-zA-Z0-9äüö_.+-]+$)", self)
        if correo_ben[1] in blacklist:
            raise ValidationError("O teu e-mail é un correo Spam. Por favor, inténteo con outro email")
        else:
             return self

class artigo_comments(models.Model):
    #on_delete significa que cando o artigo se elimina, que se elimine tamén os comentarios que están asociados co artigo.
    #artigo_key: é a foreign key que conecta o comentario co blog (artigo)
    artigo_key=models.ForeignKey(artigos, related_name="comments", on_delete=models.CASCADE)
    #A persona que escribe o comentario
    nome = models.CharField(blank=False, max_length=255)
    correo_electrónico = models.EmailField(blank=False, max_length=255, validators=[email_validation])
    comentario = models.TextField(blank=False)
    #Teño que utilizar DateField e non podo utilizar o DateTimeField porque na base de datos de Postgress
    #de Railway non me acepta o datetime field.
    date_added = models.DateField (default=datetime.now, blank=True, null=True)
    #date_added = models.DateTimeField (default=datetime.now, blank=True)

    #Esto é para que me ordene os comentarios na páxina por data
    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return (self.nome)    

#Pero eu quero que o unique_slug_generator funcione antes de que o modelo (quero dicir,os datos) son gardados.
#E dicir, antes de que os datos sexan gardados ten que cubrir o slug no field. Para tal feito o utilizao o código que está a seguir
def artigos_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator (instance)

pre_save.connect(artigos_pre_save_receiver, sender=artigos)






