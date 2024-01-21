from difflib import restore
from django.shortcuts import render, redirect

from entradas.forms import entradas_reserva_form

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages

from entradas.models import entradas_modelo
#EStou importando o paquete das expresións regulares
import re
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from django.urls import reverse


#Esta función e para enviar un email unha vez se reserve a entrada:
def send_confirm_email (request, email, name, number_tickets):
    #Con esto o que fago e que o link seax dinámico e colla o 127.0.0.1:8000 cando estamos en local e o terrameiga.bike cando está en production
    current_site = get_current_site(request)
    subject = "Reserva Confirmada"
    # message = f'Click in the following link to confirm your email and create your account http://127.0.0.1:8000/account_confirmation_email_done/{uidb64}/{token}/'
    # IMPORTANTE: As imaxes non se van a renderizar no email porque o dominio (127.0.0.1:8000), é un dominio local. No momento que metas o dominio
    # as imaxes deberíanse renderizar no email que lle chega ao user porque é un dominio seguro é hotmail/gmail/apple non o bloquea. Terás que cambiar a url no
    # arquivo de helpers.px
    message = render_to_string('email_entradas_confirmacion.html', {
        'email_browser': f'http://{current_site}' + reverse('confirmacion_reserva_email') + f'?nome_reserva={name}&numero_entradas={number_tickets}&email={email}',
        'nome': name,
        'numero_entradas' : number_tickets,
        'email' : email
    })
    #Se escribo o sender_mail así, o que fago e que aparezca o nome de "NovaEra" e así non aparece a dirección de email cando se recibe a mensaxe.
    sender_email = "Banda de Gaitas Nova Era <" + settings.EMAIL_HOST_USER + ">"
    recipient_list = [email]
    # Send the email with HTML content
    send_mail(subject, '', sender_email, recipient_list, html_message=message)
    return True

#Esta función e para enviar un email unha vez que se modificou o número de entradas
def send_modification_email (request, email, name, number_tickets):
    #Con esto o que fago e que o link seax dinámico e colla o 127.0.0.1:8000 cando estamos en local e o terrameiga.bike cando está en production
    current_site = get_current_site(request)
    subject = "Modificación da reserva"
    # message = f'Click in the following link to confirm your email and create your account http://127.0.0.1:8000/account_confirmation_email_done/{uidb64}/{token}/'
    # IMPORTANTE: As imaxes non se van a renderizar no email porque o dominio (127.0.0.1:8000), é un dominio local. No momento que metas o dominio
    # as imaxes deberíanse renderizar no email que lle chega ao user porque é un dominio seguro é hotmail/gmail/apple non o bloquea. Terás que cambiar a url no
    # arquivo de helpers.px
    message = render_to_string('email_entradas_modificacion.html', {
        'email_browser': f'http://{current_site}' + reverse('modificacion_entrada_email') + f'?nome_reserva={name}&numero_entradas={number_tickets}&email={email}',
        'nome': name,
        'numero_entradas' : number_tickets,
        'email_send_function' : email,
    })
    #Se escribo o sender_mail así, o que fago e que aparezca o nome de "NovaEra" e así non aparece a dirección de email cando se recibe a mensaxe.
    sender_email = "Banda de Gaitas Nova Era <" + settings.EMAIL_HOST_USER + ">"
    recipient_list = [email]
    # Send the email with HTML content
    send_mail(subject, '', sender_email, recipient_list, html_message=message)
    return True

# Create your views here.
def entradas_view(request, *args, **kwargs): 
  # create a form instance and populate it with data from the request:
  entradas_reserva = entradas_reserva_form(data=request.POST)
  numero_entradas_form = None
  nome_entradas_form = None
#A SEGUINTE SECCIÓN SERÁ PARA CONTABILIZAR AS ENTRADAS RESERVADAS E AS QUE FALTAN POR RESERVAR
  #Definimos o número de entradas que están reservadas
  entradas_reservadas = len(entradas_modelo.objects.values_list('numero_entradas'))
  #Esto é para traer todos o número de entradas que están reservardas
  numeroentradas_data = entradas_modelo.objects.values_list('numero_entradas')
  lista_numeroentradas=[]
  for entrada in numeroentradas_data:
    #Como me trae os correos con paréntesis e comillas, pois o que fago e eliminalos cas regular expressions
    result=re.search("[^(,']+", str(entrada))
    numero_entrada = int(result.group(0))
    lista_numeroentradas.append(numero_entrada)
  #Definimos número de entradas reservadas
  entradas_reservadas = sum(lista_numeroentradas)
  #######EIQUI É ONDE TES QUE MODIFICAR O NÚMERO DE ENTRADAS DISPOÑIBLES QUE HAI NO AUDITORIO ##########
  entradas_disponhibles= 3 - entradas_reservadas

#A SEGUINTE SECCIÓN SERÁ MANEXAR OS EMAILS E O FORM E ENVIAR A VISTA DE CONFIRMACION RESERVA OU A DE MODIFICACION RESERVA
  #Esto é para traer todos os emails que foron recollidos e que están na base de datos
  email_data = entradas_modelo.objects.values_list('correo_electrónico_entradas')
  lista_emails=[]
  for email in email_data:
    #Como me trae os correos con paréntesis e comillas, pois o que fago e eliminalos cas regular expressions
    result=re.search("[^(,']+", str(email))
    lista_emails.append(result.group(0))
  
  # if this is a POST request we need to process the form data (Todos os comentarios que nos cheguen serán POST)
  if request.method == 'POST':
    if entradas_disponhibles == 0:
      messages.error(request, 'ENTRADAS ESGOTADAS!')
      if entradas_reserva.is_valid():
      #ESto é para coller o correo que foi intrucido no form
        correo_clean = entradas_reserva.cleaned_data.get('correo_electrónico_entradas')
        #ESto é para coller o numero de entradas que foi intrucido no form
        numero_entradas_form = entradas_reserva.cleaned_data.get('numero_entradas')
        nome_entradas_form = entradas_reserva.cleaned_data.get('nome')
        apelidos_entradas_form = entradas_reserva.cleaned_data.get('apelidos')
        #Vemos se o correo introducido está contido na base de datos.
        #Se está contido na base de datos actualizamos nome, apelidos e número de entradas
        if correo_clean in lista_emails:
          #Actualización do nome, apelidos e número de entradas sempre e cando o correo esté contido na base de datos
          entradas_modelo.objects.filter(correo_electrónico_entradas=correo_clean).update(numero_entradas=numero_entradas_form, nome=nome_entradas_form, apelidos=apelidos_entradas_form)
          send_modification_email(request, correo_clean, nome_entradas_form, numero_entradas_form)
          #reverse pide unha view e devolve a url asociada a esa view IMPORTANTE: the ? character indicates the start of the query parameters
          #Without the ?, the parameters might not be interpreted correctly as query parameters by the server.
          url = reverse('modificacion_reserva') + f'?nome_reserva={nome_entradas_form}&numero_entradas={numero_entradas_form}&email={correo_clean}'
          return redirect(url)
        else:
          #No caso de que o correo non esté contido na base de datos creamos un novo rexistro
          new_entradas_reserva = entradas_reserva.save(commit=False)
          # Save the comment to the database
          new_entradas_reserva.save()
          send_confirm_email(request, correo_clean, nome_entradas_form, numero_entradas_form)
          #reverse pide unha view e devolve a url asociada a esa view IMPORTANTE: the ? character indicates the start of the query parameters
          #Without the ?, the parameters might not be interpreted correctly as query parameters by the server.
          url = reverse('confirmacion_reserva') + f'?nome_reserva={nome_entradas_form}&numero_entradas={numero_entradas_form}&email={correo_clean}'
          return redirect(url)

      # No caso de que algún dato do formulario non fose correcto, lanzamos unha mensaxe de error
      else:
        for field, errors in entradas_reserva.errors.items():
          entradas_reserva[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
        messages.error(request, 'Bótelle un ollo aos errores e inténteo de novo')

  context = {
    'entradas_reserva_form_html': entradas_reserva,
    'entradas_reservadas_view': entradas_reservadas,
    'entradas_disponhibles_view': entradas_disponhibles,
  }
  
  return render (request, 'entradas.html', context)

def confirmacion_reserva_paxina (request):
  #Collemos os valores que veñen a través da url
  nome_entradas = request.GET.get('nome_reserva', None)
  numero_entradas = request.GET.get('numero_entradas', None)
  email_entradas = request.GET.get('email', None)

  context = {
    'nome_entradas_form_html': nome_entradas,
    'numero_entradas_form_html': numero_entradas,
    'email_entradas_form_html': email_entradas
  }
  return render(request, 'pag_entradas_confirmacion.html', context)

def email_confirmacion_reserva_view (request):
  #Collemos os valores que veñen a través da url
  nome_entradas = request.GET.get('nome_reserva', None)
  numero_entradas = request.GET.get('numero_entradas', None)
  email_entradas = request.GET.get('email', None)

  context = {
    'nome_entradas_email_html': nome_entradas,
    'numero_entradas_email_html': numero_entradas,
    'email_entradas_email_html': email_entradas
  }
  return render(request, 'email_entradas_confirmacion.html', context)


def modificacion_reserva_paxina_view (request):
  #Collemos os valores que veñen a través da url
  nome_entradas = request.GET.get('nome_reserva', None)
  numero_entradas = request.GET.get('numero_entradas', None)
  email_entradas = request.GET.get('email', None)

  context = {
    'nome_entradas_form_html': nome_entradas,
    'numero_entradas_form_html': numero_entradas,
    'email_entradas_form_html': email_entradas
  }

  return render(request, 'pag_entradas_modificacion.html', context)

def email_modificacion_reserva_view (request):
  #Collemos os valores que veñen a través da url
  nome_entradas = request.GET.get('nome_reserva', None)
  numero_entradas = request.GET.get('numero_entradas', None)
  email_entradas = request.GET.get('email', None)

  context = {
    'nome_entradas_email_html': nome_entradas,
    'numero_entradas_email_html': numero_entradas,
    'email_entradas_email_html': email_entradas
  }

  return render(request, 'email_entradas_modificacion.html', context)
