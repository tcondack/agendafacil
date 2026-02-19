from django import forms
from .models import Usuario, feedback_cliente
from django.contrib.auth.forms import UserCreationForm

## criação de usuário
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'email',
            'CPF',
            'telefone',
            'foto_perfil',
            'password1',
            'password2',
        ]
       
    def save(self, commit=True):
        user = super().save(commit=False)


        CPF = self.cleaned_data['CPF']  # Usando o CPF como nome de usuário
        user.username = CPF
        user.tipo_usuario = 'cliente'  # Definindo o tipo de usuário como 'cliente' por padrão
        user.is_active = True  # Ativando o usuário imediatamente
        if commit:
            user.save()
        return user

## Edição perfil cliente    
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'email',
            'telefone',
            'foto_perfil',
            'cep',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        ]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = feedback_cliente
        fields = ['agendamento','nota', 'comentario']
        labels = {
            'agendamento': 'Qual atendimento você deseja avaliar?',
            'nota': 'Nota',
            'comentario': 'Conte sua experiência"',
        }
        widgets = {
            'comentario': forms.Textarea(attrs={
                'placeholder': 'Deixe seu comentário aqui...',
                'class': 'form-control'
            })
        }
