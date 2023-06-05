from django import forms
from .models import newsletter_email

class form_newsletter(forms.ModelForm):
    class Meta:
        model = newsletter_email
        fields = [ 'email_subscriptor' ]
        widgets = {
            'email_subscriptor': forms.EmailInput (attrs = {'class': 'form-control', 'placeholder':'Ex: "pepe@gmail.com"'})
        }