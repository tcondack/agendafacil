from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'email',
            'CPF',
            'telefone',
            'foto_perfil'
        ]
       
    def save(self, commit=True):
        user = super().save(commit=False)

        user.tipo_usuario = 'cliente'  # Definindo o tipo de usuário como 'cliente' por padrão

        user.username = self.cleaned_data['CPF']  # Usando o CPF como nome de usuário
        if commit:
            user.save()
        return user