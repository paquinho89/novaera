from django.shortcuts import render, redirect

from newsletter.form import form_newsletter

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages

# Create your views here.

# Create your views here.
def home_page_view(request):
  # create a form instance and populate it with data from the request:
  newsletter_email = form_newsletter(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if newsletter_email.is_valid():
      # Create Comment object but don't save to database yet
      new_subscriber_email = newsletter_email.save(commit=False)
      # Save the comment to the database
      new_subscriber_email.save()
      #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
      messages.success(request, 'Graciñas por subscribirte a nosa newletter. Non seremos moi pesados.')
      #artigos_content e que para que me retorne a vista do blog. Vaste o archivo das urls e buscas a url que queiras que che retorne
      return redirect('home_page')

    # if a GET (or any other method) we'll create a blank form
    else:
      #messages.error(request, "Porfavor, introduza un correo electrónico válido")
      #Comentando a seguinte línea o formulario non se vacía despois do error. 
      #newsletter_email = form_newsletter()
      # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
      # asigne o formato de error (O borde en vermello)
      for field, errors in newsletter_email.errors.items():
        newsletter_email[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
        print (errors)
      #Esto imprime o error xusto debaixo do cajetín para inserir o correo
      messages.error(request, newsletter_email.errors)
      #messages.error(request, "Insira un enderezo de correo electrónico válido!")
      print(newsletter_email.errors)
      
        
  context = {
        'form_newsletter_home_page':newsletter_email,
  }

  return render (request, 'home_page.html', context)

