from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Usuario(AbstractUser):
    Usuario_escolha =(
        ('CLIENTE', 'Cliente'),
        ('ATENDENTE', 'Atendente'),
    )

    tipo_usuario = models.CharField(
        max_length=10,
        choices=Usuario_escolha,
        default='CLIENTE',
    )

    CPF = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True   
    )

    foto_perfil = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True
    )
    cep = models.CharField(max_length=9, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=40, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username  
   
class agendamento(models.Model):
    cliente = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE,
    related_name='agendamentos')

    data = models.DateField()
    horario = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.data} - {self.horario}'

    STATUS_CHOICES = (
        ('AGENDADO', 'Agendado'),
        ('CANCELADO', 'Cancelado'),
        ('CONFIRMADO', 'Confirmado'),
        ('ATENDIDO', 'Atendido'),
       )
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='AGENDADO',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
     return f"{self.cliente} - {self.data} {self.horario}"


