from pdb import post_mortem
from django.shortcuts import redirect, render

from .models import artigos, artigo_comments, autores
from .forms import CommentForm

#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages


# Create your views here.
def artigos_list_view (request):
  #Vamos a unir as 2 tablas (artigos & autores) para ter todo nunha sola query set e poder recorrela toda desde o html
  #IMPORTANTE: O select_related é como estar facendo un inner join. Estás unindo a tabla de artigos ca de autores pola columna que teñan en común ("author").
  artigos_autores_queryset = artigos.objects.select_related('author').all()
  #Esto é para ver como sería a sql query que o select_related('author') está a facer.
  #print(str(artigos_autores_queryset.query))
    
  context = {
      'artigos_autores': artigos_autores_queryset,
    }
  return render (request, 'artigo_list.html', context)
   

# Esto é a vista específica do contido de cada artigo
def artigos_content_view(request, slug=None, *args, **kwargs):
  #Eiqui estamos collendo o instance slug do modelo (que o slug é o mesmo co título)
  artigo_instance = artigos.objects.get(slug=slug)
  #Eiqui, a través do slug, collemos o pk do queryset, e facemos[0] para coller o primeiro elemento da lista.
  #OLLO. Para levar os elementos do modelo o html, temos que ir solo co nome do autor. Por eso collo o primeiro elemento da lista co [0]
  pk_autor= artigos.objects.filter(slug=slug).values_list('author', flat='True')[0]
  #Eiqui collemos a query set co pk que obtimos na anterior línea de código.
  autor_blog_qs= autores.objects.filter(pk=pk_autor)[0]
  #Eiqui collemos todas as querysets (comentarios) que conteñan o artigo title que estamos a visitar
  comments_qs = artigo_comments.objects.filter(artigo_key=artigo_instance)
  #Vamos a contar o número de comentarios para poñelos na páxina ao lado do título de comentarios
  number_comments=artigo_comments.objects.all().filter(artigo_key=artigo_instance).count()
  # create a form instance and populate it with data from the request:
  comment_form = CommentForm(data=request.POST)
  # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
  if request.method == 'POST':
    # check whether it's valid:
    if comment_form.is_valid():
      # Create Comment object but don't save to database yet
      new_comment = comment_form.save(commit=False)
      # esto é para que asigne o artigo_key do comentario co seu correspondente blog. Lembra que o artigo_key é o que relaciona o comentario co blog
      new_comment.artigo_key = artigo_instance
      # Save the comment to the database
      new_comment.save()
       #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
      messages.success(request, 'Parabéns, o seu comentario foi engadido!')
      #artigos_content e que para que me retorne a vista do blog
      return redirect('artigos_content', slug=artigo_instance.slug)
    
    

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
    'artigo_detail': artigo_instance,
    'form':comment_form,
    'autor':autor_blog_qs,
    'comments_blog' : comments_qs,
    'number_comments' : number_comments
  }

  return render (request, 'artigos_content.html', context)







    
