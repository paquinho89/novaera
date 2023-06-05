from django.contrib import admin

# Register your models here.

from entradas.models import entradas_modelo

# Register your models here.
#admin.site.register(entradas_modelo)


#Estp é para configurar o panel de administración de django é que aparezan os seguintes campos
#no panel.
#O ordering é para que ordene os campos por data do rexitro (o "-" é para sea o orden descendente)
#O search field é para facer unha búsqueda, neste caso por nome de contratante.
@admin.register(entradas_modelo)
class contratacion_datos_admin(admin.ModelAdmin):
    list_display = ['nome', 'apelidos', 'correo_electrónico_entradas', 'numero_entradas']
    ordering = ['-data_rexistro']
