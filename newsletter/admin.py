from django.contrib import admin
from newsletter.models import newsletter_email

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import admin
import os

#I create an admin action to send emails to the subscribers whenever I want
def send_newsletter (modeladmin, request, queryset):
    emails = list(queryset.values_list('email_subscriptor', flat=True))
    subject = "Banda de Gaitas Nova Era - DEZ"
    from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string("newsletter_1_email.html", {
        "title": "DEZ",
        "date": "7 de Decembro 2025 ás 19:30h",
        "location": "Auditorio Municipal de Ourense",
        "ticket_url": "https://entradas.ataquilla.com/es/ventaentradas/conciertos/251-auditorio-municipal-de-ourense/x3ajp45k-dez",
    })

    # Plain text fallback (for clients that don’t support HTML)
    text_content = (
        "Banda de Gaitas Nova Era presenta: DEZ\n"
        "7 de Decembro 2025 ás 19:30h\n"
        "Auditorio Municipal de Ourense\n"
        "Mercar entradas: https://entradas.ataquilla.com/es/ventaentradas/conciertos/251-auditorio-municipal-de-ourense/x3ajp45k-dez"
    )

    # Create the email with both text and HTML alternatives
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=["paquinho89@gmail.com"],
        bcc=emails  # use BCC so recipients don't see each other
    )
    msg.attach_alternative(html_content, "text/html")

    # Attach the banner image inline
    banner_path = os.path.join(settings.BASE_DIR, "NovaEra", "static", "dez_newsletter_attached.png")
    with open(banner_path, "rb") as f:
        msg_image = f.read()
    msg.attach("NovaEra_cartel.png", msg_image, "image/png")
    # Tell Django this is a multipart/related message (so inline images work)
    msg.mixed_subtype = 'related'

    # Attach the banner image inline
    banner_path = os.path.join(settings.BASE_DIR, "NovaEra", "static", "dez_logo.jpg")
    with open(banner_path, "rb") as f:
        msg_image = f.read()
    msg.attach("NovaEra_logo.png", msg_image, "image/png")
    # Tell Django this is a multipart/related message (so inline images work)
    msg.mixed_subtype = 'related'

    # Send email
    msg.send(fail_silently=False)

    # ESta é a mensaxe que sale no administrador cando se envían as mensaxes
    modeladmin.message_user(request, f"Newsletter sent to {len(emails)} recipients.")

class newsletteradmin (admin.ModelAdmin):
    actions = [send_newsletter] 


# Register your models here.
admin.site.register(newsletter_email,  newsletteradmin)


