from django.contrib import admin

# Register your models here.
from .models import autores, artigos, artigo_comments


admin.site.register(autores)
#admin.site.register(artigos)
admin.site.register(artigo_comments)


#Estp é para configurar o panel de administración de django é que aparezan os seguintes campos
#no panel.
#O ordering é para que ordene os campos por data do rexitro (o "-" é para sea o orden descendente)
#O search field é para facer unha búsqueda, neste caso por nome de contratante.
@admin.register(artigos)
class contratacion_datos_admin(admin.ModelAdmin):
    list_display = ['artigos_title', 'author', 'artigos_date']
    ordering = ['-artigos_date']
    #search_fields = ['artigos_title']