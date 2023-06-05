from difflib import restore
from django.shortcuts import render, redirect

from entradas.forms import entradas_reserva_form

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages

from entradas.models import entradas_modelo
#EStou importando o paquete das expresións regulares
import re

# Create your views here.
def entradas_view(request, *args, **kwargs): 
  # create a form instance and populate it with data from the request:
  entradas_reserva = entradas_reserva_form(data=request.POST)
  
  #Esto é para traer todos os emails que foron recollidos e que están na base de datos
  email_data = entradas_modelo.objects.values_list('correo_electrónico_entradas')
  lista_emails=[]
  for email in email_data:
    #Como me trae os correos con paréntesis e comillas, pois o que fago e eliminalos cas regular expressions
    result=re.search("[^(,']+", str(email))
    lista_emails.append(result.group(0))
  
  # if this is a POST request we need to process the form data (Todos os comentarios que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
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
        #Esto é para que me mostre a mensaxe de que se actualizou a solicitude, xa que o correo xa estaba contido na base de datos
        messages.success(request, ('Os seus datos foron actualizados: %(numero_entradas)s entradas reservadas a nome de %(nome)s %(apelidos)s co seguinte correo: %(correo)s')
                %{'numero_entradas':numero_entradas_form, 'nome':nome_entradas_form, 'apelidos':apelidos_entradas_form, 'correo':correo_clean})
      else:
        #No caso de que o correo non esté contido na base de datos creamos un novo rexistro
        new_entradas_reserva = entradas_reserva.save(commit=False)
        # Save the comment to the database
        new_entradas_reserva.save()
        #Esto é para que me mostre a mensaxe de que se creou un novo rexistro
        messages.success(request, ('Parabéns! Ten %(numero_entradas)s entradas reservadas a nome de %(nome)s %(apelidos)s. Vémonos no espectáculo')
                %{'numero_entradas':numero_entradas_form, 'nome':nome_entradas_form, 'apelidos':apelidos_entradas_form})
      
      

      #artigos_content e que para que me retorne a vista do blog. Vaste o archivo das urls e buscas a url que queiras que che retorne
      return redirect('reserva_entradas')

    # No caso de que algún dato do formulario non fose correcto, lanzamos unha mensaxe de error
    else:
      #messages.error(request, "Porfavor, introduza un correo electrónico válido")
      #Comentando a seguinte línea o formulario NON se vacía despois do error. 
      #newsletter_email = form_newsletter()
      # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
      # asigne o formato de error (O borde en vermello)
      for field, errors in entradas_reserva.errors.items():
        entradas_reserva[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
      
      messages.error(request, entradas_reserva.errors)

#A SEGUINTE SECCIÓN SERÁ PARA CONTABILIZAR AS ENTRADAS RESERVADAS E AS QUE FALTAN POR RESERVAR

  #Definimos o número de entradas que están reservadas
  entradas_reservadas = len(entradas_modelo.objects.values_list('numero_entradas'))
  print (entradas_modelo.objects.values_list('numero_entradas') )

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
  # Definimos o número de entradas dispoñibles ######EIQUI É ONDE TES QUE MODIFICAR O NÚMERO DE ENTRADAS DISPOÑIBLES QUE HAI NO AUDITORIO ##########
  entradas_disponhibles=200 - entradas_reservadas

  context = {
    'form_entradas_reserva':entradas_reserva,
    'entradas_reservadas_view': entradas_reservadas,
    'entradas_disponhibles_view': entradas_disponhibles
  }
  
  return render (request, 'entradas.html', context)
