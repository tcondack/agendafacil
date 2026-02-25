from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Usuario(AbstractUser):
    Usuario_escolha =(
        ('CLIENTE', 'Cliente'),
        ('ATENDENTE', 'Atendente'),
        ('ADMIN', 'Admin'),
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
   
class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('AGENDADO', 'Agendado'),
        ('ATENDIDO', 'Atendido'),
        ('CANCELADO', 'Cancelado'),
        ('FALTOU', 'Faltou'),
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        limit_choices_to={'tipo_usuario': 'CLIENTE'}
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='AGENDADO'
        )
    criado_em = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"{self.cliente} - {self.get_status_display()} ({self.criado_em.strftime('%d/%m/%Y')})"
   
class FeedbackCliente(models.Model):
    agendamento = models.OneToOneField(
      Agendamento, 
      on_delete=models.CASCADE, 
      related_name='feedback'
    )
    cliente = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE,
       related_name='feedbacks_enviados'
    )
    atendente = models.ForeignKey(
      settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks_recebidos',
        null=True,    
        blank=True,
    )
    comentario = models.TextField("Avaliação do Cliente")

    nota = models.PositiveIntegerField(
        "Nota",
        choices=[(1, "1 ⭐"), (2, "2 ⭐"), (3, "3 ⭐"), (4, "4 ⭐"), (5, "5 ⭐")]
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.cliente.first_name} - {self.nota}⭐"
   
class Atendimento(models.Model):
    agendamento = models.OneToOneField(
        Agendamento, 
        on_delete=models.CASCADE,
        related_name='atendimento'
    )
    atendente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='atendimentos_realizados',
        limit_choices_to={'tipo_usuario': 'ATENDENTE'}
    )
    descricao_procedimento = models.TextField("Descrição do Atendimento")
    observacoes_atendimento = models.TextField("Observações do Atendimento", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Atendimento de {self.atendente.first_name} - {self.agendamento.data} {self.agendamento.horario}"
    
class HorarioAtendimento(models.Model):
    data = models.DateField()
    horario = models.TimeField()

    atendente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='horarios_atendimentos',
        limit_choices_to={'tipo_usuario': 'ATENDENTE'}
    )
    disponivel = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('data', 'horario', 'atendente')
        ordering = ['data', 'horario']  
    def __str__(self):
        return f"{self.data} {self.horario} - {self.atendente}"
    