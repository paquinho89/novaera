from django.shortcuts import render

from artigos.models import artigos

# def home_page(request):
#     return render(request, 'pages/home.html')

# novaera/views.py
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
############

def obra_social(request):
  return render(request, 'obra_social.html')


def information_view(request):
  return render (request, 'informacion.html')
