from django.shortcuts import render

from django.http import FileResponse
import os

from NovaEra.settings import BASE_DIR

# Create your views here.

def pdf_view(request):
    #Esta sería a ruta para renderizar o archivo en local e en Heroku
    filepath = os.path.join(BASE_DIR, 'NovaEra\static\Díptico_Álvaro_Rúa.pdf')
    #filepath = 'C:/Users/falvarez/OneDrive - McAfee/NovaEra/NovaEra/static/Díptico_Álvaro_Rúa.pdf'
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')