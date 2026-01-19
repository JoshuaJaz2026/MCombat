from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

class ValidarCorreoResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # BUSCAMOS EN LA BASE DE DATOS
        if not User.objects.filter(email=email).exists():
            # Si no existe, lanzamos el error en pantalla
            raise forms.ValidationError("❌ Este correo NO está registrado en nuestro sistema.")
        
        return email