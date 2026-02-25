from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Agendamento, FeedbackCliente
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
    list_display = ('cliente', 'get_data', 'get_horario', 'criado_em')
    list_filter = ('status',)
    def get_data(self, obj):
            return obj.horario.data
            get_data.short_description = 'Data'

    def get_horario(self, obj):
            return obj.horario.horario
            get_horario.short_description = 'Horário'


@admin.register(FeedbackCliente)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'agendamento', 'nota', 'criado_em')    