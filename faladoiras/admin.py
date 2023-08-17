from django.contrib import admin

# Register your models here.
from .models import faladoiras, faladoiras_comments


admin.site.register(faladoiras)
admin.site.register(faladoiras_comments)


