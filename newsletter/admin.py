from django.contrib import admin
from newsletter.models import newsletter_email

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import admin
import os

def send_newsletter(modeladmin, request, queryset):
    emails = list(queryset.values_list('email_subscriptor', flat=True))
    subject = "Banda de Gaitas Nova Era - DEZ"
    from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string("newsletter_1_email.html", {
        "title": "DEZ",
        "date": "7 de Decembro 2025 ás 19:30h",
        "location": "Auditorio Municipal de Ourense",
        "ticket_url": "https://entradas.ataquilla.com/es/ventaentradas/conciertos/251-auditorio-municipal-de-ourense/x3ajp45k-dez",
    })

    text_content = (
        "Banda de Gaitas Nova Era presenta: DEZ\n"
        "7 de Decembro 2025 ás 19:30h\n"
        "Auditorio Municipal de Ourense\n"
        "Mercar entradas: https://entradas.ataquilla.com/es/ventaentradas/conciertos/251-auditorio-municipal-de-ourense/x3ajp45k-dez"
    )

    for email in emails:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")

        # Enviar o correo individual
        msg.send(fail_silently=False)

    modeladmin.message_user(request, f"Newsletter sent to {len(emails)} recipients.")


class newsletteradmin (admin.ModelAdmin):
    actions = [send_newsletter] 


# Register your models here.
admin.site.register(newsletter_email,  newsletteradmin)


