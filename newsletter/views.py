from django.shortcuts import render, redirect

from newsletter.form import form_newsletter, form_newsletter_unsubscribe
from newsletter.models import newsletter_email
#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages

# Create your views here.
def home_page_view(request):
  # create a form instance and populate it with data from the request:
  newsletter_email_form = form_newsletter(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if newsletter_email_form.is_valid():
      email_input = newsletter_email_form.cleaned_data['email_subscriptor']
      #Se o correo non está na nosa base de datos, engadímolo
      if not newsletter_email.objects.filter(email_subscriptor = email_input).exists():
        # Create Comment object but don't save to database yet
        new_subscriber_email = newsletter_email_form.save(commit=False)
        # Save the comment to the database
        new_subscriber_email.save()
        #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
        messages.success(request, 'Graciñas por subscribirte a nosa newletter. Non seremos moi pesados.')
        #artigos_content e que para que me retorne a vista do blog. Vaste o archivo das urls e buscas a url que queiras que che retorne
        return redirect('home_page')
      #Se o correo XA está na nosa base de datos, non o engadimos
      else:
        messages.success(request, 'Moitas grazas pero o seu correo xa está na nosa base de datos')
      #Cualquer outra opción, mostramos o erro
    else:
      #messages.error(request, "Porfavor, introduza un correo electrónico válido")
      #Comentando a seguinte línea o formulario non se vacía despois do error. 
      #newsletter_email = form_newsletter()
      # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
      # asigne o formato de error (O borde en vermello)
      for field, errors in newsletter_email_form.errors.items():
        newsletter_email_form[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
        print (errors)
      #Esto imprime o error xusto debaixo do cajetín para inserir o correo
      messages.error(request, newsletter_email_form.errors)
      #messages.error(request, "Insira un enderezo de correo electrónico válido!")
        
  context = {
        'form_newsletter_home_page':newsletter_email_form,
  }

  return render (request, 'home_page.html', context)

#Vista para a landing page da xente que se unsubscribe
def newsletter_unsubscribe (request):
  unsubscribe_email_form = form_newsletter_unsubscribe(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if unsubscribe_email_form.is_valid():
      email_input = unsubscribe_email_form.cleaned_data['email_subscriptor']
      #This is to check if the email which was introduced in the text box exists on the data base. If it does not exist, no action is performed.
      if newsletter_email.objects.filter(email_subscriptor = email_input).exists():
        # Delete the email from the database.
        unsubscriber = newsletter_email.objects.get(email_subscriptor=email_input)
        #Set the subscribed to False (red cross in the data base)
        unsubscriber.delete()
        #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
        messages.success(request, 'O seu correo foi eliminado da nosa base de datos')
        return redirect('home_page')
      else:
        messages.error(request, 'O correo que introduciu non se atopa na nosa base de datos')

  context = {
        'form_unsubscribed_newsletter':unsubscribe_email_form,
  }
  return render(request, "unsubscribers_landingpage.html", context)


#Vista para ver a landing page que está no correo que se envía
def newsletter_landingpage (request):
  return render(request, 'newsletter_1_landingpage.html')

