"""NovaEra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from NovaEra.views import information_view, obra_social
from artigos.views import artigos_list_view, artigos_content_view
from banda_contratacion.views import contratacion_view
from newsletter.views import home_page_view
from entradas.views import entradas_view
from render_pdf.views import pdf_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page_view, name='home_page'),
    path('obra_social/', obra_social, name='obra_social'),
    path('contratación/', contratacion_view, name='contratación'),
    path('informacion/', information_view, name='informacion'),
    path('artigos/', artigos_list_view, name='artigos'),
    # The P is Python identifier for a named capture group. You will see P in regex used in django
    # ? you want to match either one or zero occurrences of this pattern
    # \d matches any digit
    # + signifies that there must be at least 1 or more digits in the number
    # $ simboliza o final da cadena. A partir de ahí non admite máis texto
    #re_path('artigos/(?P<id>\d+)/$', artigos_content_view, name='artigos_content'),
    re_path('artigos/(?P<slug>[\w-]+)/$', artigos_content_view, name='artigos_content'),
    path('entradas/', entradas_view, name='reserva_entradas'),
    path('record_guinnes/', TemplateView.as_view(template_name = "record_guinnes.html"), name='record_guinnes'),
    #Este é a url para renderizar un pdf
    path('pdf/', pdf_view, name='pdf')
]
#If DEBUG is false, you can't serve locally. If true, it will serve locally.
#These two lines allow the development server to serve user-uploaded files in the MEDIA_ROOT directory.
#settings.DEBUG check if we are in debug mode (development_mode) or not (production_mode).
#Mañá mírate esta páxina
# https://docs.djangoproject.com/en/1.11/howto/static-files/#serving-files-uploaded-by-a-user-during-development
if settings.DEBUG:
    urlpatterns = list(urlpatterns) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = list(urlpatterns) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)