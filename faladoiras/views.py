from pdb import post_mortem
from django.shortcuts import redirect, render

from .models import faladoiras, faladoiras_comments
from .forms import CommentForm

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages


# Create your views here.  

# Esto é a vista específica do contido de cada artigo
def faladoiras_content_view(request, slug=None, *args, **kwargs):
  #Eiqui estamos collendo o instance slug do modelo (que o slug é o mesmo co título)
  faladoiras_instance = faladoiras.objects.get(slug=slug)
  #Eiqui collemos todas as querysets (comentarios) que conteñan o artigo title que estamos a visitar
  comments_qs = faladoiras_comments.objects.filter(artigo_key=faladoiras_instance)
  #Vamos a contar o número de comentarios para poñelos na páxina ao lado do título de comentarios
  number_comments=faladoiras_comments.objects.all().filter(artigo_key=faladoiras_instance).count()
  # create a form instance and populate it with data from the request:
  comment_form = CommentForm(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if comment_form.is_valid():
      # Create Comment object but don't save to database yet
      new_comment = comment_form.save(commit=False)
      # esto é para que asigne o artigo_key do comentario co seu correspondente blog. Lembra que o artigo_key é o que relaciona o comentario co blog
      new_comment.faladoiras_key = faladoiras_instance
      # Save the comment to the database
      new_comment.save()
       #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
      messages.success(request, 'Parabéns, o seu comentario foi engadido!')
      #artigos_content e que para que me retorne a vista do blog
      return redirect('faladoiras_content', slug=faladoiras_instance.slug)
    
    # if a GET (or any other method) we'll create a blank form
    #EIQUI TES QUE DICIR QUE O FORMULARIO NON É VÁLIDO E NON ESTÁ EN BLANCO.

    else:
      messages.error(request, comment_form.errors)
      #Comentando a seguinte línea o formulario non se vacía despois do error.
      #comment_form = CommentForm()
      # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
      # asigne o formato de error (O borde en vermello)
      for field in comment_form.errors:
        comment_form[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})

      

  context = {
    'artigo_detail': faladoiras_instance,
    'form':comment_form,
    'comments_blog' : comments_qs,
    'number_comments' : number_comments
  }

  return render (request, 'faladoiras_content.html', context)







    
