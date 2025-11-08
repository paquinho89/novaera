from django.contrib import admin

from newsletter.models import newsletter_email, newsletteradmin


# Register your models here.
admin.site.register(newsletter_email, newsletteradmin)


