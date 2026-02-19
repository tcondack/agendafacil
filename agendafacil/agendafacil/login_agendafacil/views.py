from urllib import request

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UsuarioForm, UsuarioUpdateForm, FeedbackForm
from .models import Usuario, Agendamento
from datetime import date
from django.contrib import messages
from django.views.decorators.http import require_POST

def index_login(request):
    return render(request, 'login_agendafacil/index_login.html')


def cadastro_cliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Define username como email
            user.username = user.email
            user.save()
            return redirect('login')
    else:
        form = UsuarioForm()

    return render(request, 'login_agendafacil/cadastro_cliente.html', {'form': form})


@login_required
def redirect_pos_login(request):

    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        return redirect('painel_admin')

    elif request.user.tipo_usuario == 'ATENDENTE':
        return redirect('painel_atendente')

    elif request.user.tipo_usuario == 'CLIENTE':
        return redirect('painel_cliente')

    else:
        return redirect('painel_cliente')
    

    ## Paines de acordo com o tipo de usuário

##PAINEIS ADMIN    
@login_required
def painel_admin(request):
    return render(request, 'login_agendafacil/painel_admin.html')
@login_required
def dados_admin(request):
    return render(request, 'login_agendafacil/dados_admin.html')
@login_required
def gerenciamento_usuarios(request):
    return render(request, 'login_agendafacil/gerenciamento_usuarios.html')

## PAINÉIS COLABORADOR
@login_required
def painel_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    
    hoje = date.today()
    agendamentos = Agendamento.objects.filter(
        data = hoje
    ).order_by('horario')
    
    context = {
        'agendamentos': agendamentos,
        'hoje': hoje
    }

    return render(request, 'login_agendafacil/painel_atendente.html', context)
@login_required
def perfil_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/perfil_atendente.html')
@login_required
def atendimento_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/atendimento_atendente.html')
@login_required
def dados_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/dados_atendente.html')


## alteração status agendamento
@login_required
def alterar_status(request, agendamento_id, status):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    
    agendamento = get_object_or_404(Agendamento, id=agendamento_id) 
    status_validos = ['CONFIRMADO', 'ATENDIDO', 'FALTOU']
    if status not in status_validos:
        return redirect('painel_atendente')

    agendamento.status= status
    agendamento.save()
    return redirect('painel_atendente')





##paineis cliente
@login_required
def painel_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/painel_cliente.html')


@login_required
def perfil_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil_cliente')
    else:
        form = UsuarioUpdateForm(instance=request.user)
        
    return render(request, 'login_agendafacil/perfil_cliente.html', {'form': form})


@login_required
def agendamento_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/agendamento_cliente.html')


@login_required
def feedback_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    
    agendamentos= Agendamento.objects.filter(cliente=request.user, status='ATENDIDO')
    
    if not agendamentos.exists():
        messages.warning(request, "Você ainda não possui atendimentos concluídos para avaliar.")
        return redirect('painel_cliente')
    

    agendamentos = Agendamento.objects.filter(cliente=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.cliente = request.user
            feedback.save()
            return redirect('painel_cliente')
    else:        form = FeedbackForm()
    form.fields['agendamento'].queryset = agendamentos

    return render(request, 'login_agendafacil/feedback_cliente.html', {'form': form})   


@login_required
def dados_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/dados_cliente.html')


## agendamento_cliente
@login_required
def agendamento_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect ('redirect_pos_login')
    
    if request.method == 'POST':
        data = request.POST.get('data')
        horario = request.POST.get('horario')

        Agendamento.objects.create(
            cliente=request.user,
            data=data,
            horario=horario
        )
        return redirect('painel_cliente')
    return render(request, 'login_agendafacil/agendamento_cliente.html')

##
@login_required
def painel_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    agendamentos = Agendamento.objects.filter(
        cliente=request.user
    ).order_by('-data', '-horario')

    return render(request, 'login_agendafacil/painel_cliente.html', {
        'agendamentos': agendamentos
    })
    return render(request, 'login_agendafacil/painel_cliente.html', {'agendamentos': agendamentos})
    
