from django.db import models
from django.contrib.auth.models import AbstractUser


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
    def __str__(self):
        return self.username
    