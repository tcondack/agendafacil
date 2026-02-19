from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Agendamento, feedback_cliente
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('tipo_usuario',)}),
        ('Permissões', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'tipo_usuario', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'horario', 'criado_em')
    list_filter = ('data',)
    search_fields = ('cliente__username',)

@admin.register(feedback_cliente)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'agendamento', 'nota', 'criado_em')    