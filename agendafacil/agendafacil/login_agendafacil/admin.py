from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, agendamento
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


@admin.register(agendamento)
class agendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'horario', 'criado_em')
    list_filter = ('data',)
    search_fields = ('cliente__username',)