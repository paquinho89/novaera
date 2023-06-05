from ast import Not
from django.shortcuts import render, redirect
from banda_contratacion.models import contratacion_datos
from .form import contratacionForm
#Pae

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages
#Paquete para enviar o email
from django.core.mail import send_mail

# Create your views here.
def contratacion_view(request):
  # create a form instance and populate it with data from the request:
  contratacion_form = contratacionForm(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if contratacion_form.is_valid():
      # Create Comment object but don't save to database yet
      new_contratacion_entry = contratacion_form.save(commit=False)
      # Save the comment to the database
      new_contratacion_entry.save()
      #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
      messages.success(request, 'Graciñas por contactar con nós!. En breve nos poremos en contacto con vostede')
      #artigos_content e que para que me retorne a vista do blog. Vaste o archivo das urls e buscas a url que queiras que che retorne

      #send an email
      #Collo os campos que se completan do formulario que me fan falta para meter no email
      contratante_eleccion_banda = request.POST.get('toda_banda', '-')
      contratante_eleccion_cuarteto = request.POST.get('cuarteto', '-')
      contratante_eleccion_terceto_1 = request.POST.get('terceto_opcion_1', '-')
      contratante_eleccion_terceto_2 = request.POST.get('terceto_opcion_2', '-')
      contratante_eleccion_duo_1 = request.POST.get('duo_opcion_1', '-')
      contratante_eleccion_duo_2 = request.POST.get('duo_opcion_2', '-')
      contratante_eleccion_solista = request.POST.get('conxunto', '-')
      contratante_tipoevento = request.POST['tipo_evento']
      contratante_data = request.POST['data_evento']
      contratante_lugar = request.POST['lugar_evento']
      contratante_telefono = request.POST['teléfono']
      contratante_nome = request.POST['nome']
      contratante_email = request.POST['correo_electrónico']
      contratante_info = request.POST['mais_info']
      send_mail(
        'Nova_Actuación - ' + contratante_nome , #subject
        "CONXUNTO SELECCIONADO:\n" +
        "Banda: " + contratante_eleccion_banda + "\n"
        "Cuarteto: " + contratante_eleccion_cuarteto + "\n" +
        "Terceto_opcion_1: " + contratante_eleccion_terceto_1 + "\n" +
        "Terceto_opcion_2: " + contratante_eleccion_terceto_2 + "\n" +
        "Duo_opcion_1: " + contratante_eleccion_duo_1 + "\n" +
        "Duo_opcion_2: " + contratante_eleccion_duo_2 + "\n" +
        "Solista: " + contratante_eleccion_solista + "\n" +
        "TIPO EVENTO: " + contratante_tipoevento +  "\n" +
        "DATA: " + contratante_data + "\n" +
        "LUGAR: " + contratante_lugar + "\n" +
        "TELEFONO: " + contratante_telefono + "\n" +
        "NOME: " + contratante_nome + "\n" +
        "EMAIL: " + contratante_email + "\n" +
        "MAIS_INFO: " + contratante_info, #message
        contratante_email, #from_email
        ['paquinho89@gmail.com', 'paquinho89@hotmail.com'], #To Email
        fail_silently = True
      )

      return redirect('contratación')
    else:
      messages.error(request, contratacion_form.errors)
      #Comentando a seguinte línea o formulario non se vacía despois do error. 
      #contratacion_form = contratacionForm()
      #return redirect('contratación')
      # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
      # asigne o formato de error (O borde en vermello)
      for field_form in contratacion_form.errors:
        contratacion_form[field_form].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
      #Esto é porque cambia o formato do último checkbox, e desta forma pois poño as mismas dimensions que debe de ter
      contratacion_form['conxunto'].field.widget.attrs.update({'style':'width:25px; height:25px; background-color:red; border-width: medium'})
  context = {
        'form':contratacion_form
  }
  return render (request, 'contratación.html', context)

