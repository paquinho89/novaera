from django.contrib import admin

from banda_contratacion.models import contratacion_datos

# Register your models here.
#admin.site.register(contratacion_datos)

#Estp é para configurar o panel de administración de django é que aparezan os seguintes campos
#no panel.
#O ordering é para que ordene os campos por data do rexitro (o "-" é para sea o orden descendente)
#O search field é para facer unha búsqueda, neste caso por nome de contratante.
@admin.register(contratacion_datos)
class contratacion_datos_admin(admin.ModelAdmin):
    list_display = ['nome', 'data_rexistro', 'data_evento', 'correo_electrónico', 'contestado']
    ordering = ['-data_rexistro']
    search_fields = ['nome']

