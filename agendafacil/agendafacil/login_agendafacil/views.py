from urllib import request

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UsuarioForm, UsuarioUpdateForm, FeedbackForm, AtendimentoForm
from .models import HorarioAtendimento, Usuario, Agendamento, FeedbackCliente
from datetime import date
from django.contrib import messages
from django.views.decorators.http import require_POST

def index_base (request):
    return render(request, 'app_agenda_facil/index.html')

def index_login(request):
    return render(request, 'login_agendafacil/index_login.html')

def esqueci_senha(request):
    return render(request, 'login_agendafacil/esqueci_senha.html')

def cadastro_cliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
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
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')
    if request.method == 'POST':
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        atendente_id = request.POST.get('atendente')

        if data and horario and atendente_id:
            HorarioAtendimento.objects.create(
                data=data,
                horario=horario,
                atendente_id=atendente_id,
                disponivel=True
            )
            messages.success(request, 'Agendamento criado com sucesso!')
        else:
            messages.error(request, 'Preencha todos os campos.')
        return redirect('painel_admin')

    context = {
        'total_agendamentos': Agendamento.objects.count(),
        'total_clientes': Usuario.objects.filter(tipo_usuario='CLIENTE').count(),
        'total_atendentes': Usuario.objects.filter(tipo_usuario='ATENDENTE').count(),
        'agendamentos_hoje': Agendamento.objects.filter(horario__data=date.today()).order_by('horario__horario'),
        'atendentes': Usuario.objects.filter(tipo_usuario='ATENDENTE').order_by('first_name'),
        'horarios_disponiveis': HorarioAtendimento.objects.filter(disponivel=True).order_by('data', 'horario'),  
    }
    return render(request, 'login_agendafacil/painel_admin.html', context)

@login_required
def remover_horario(request, horario_id):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')
    horario = get_object_or_404(HorarioAtendimento, id=horario_id)
    horario.delete()
    messages.success(request, 'Horário removido com sucesso!')
    return redirect('painel_admin')

@login_required
def dados_admin(request):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')

    from django.db.models import Count, Q

    agendamentos_por_data = (
        Agendamento.objects
        .values('horario__data')
        .annotate(
            agendados=Count('id'),
            atendidos=Count('id', filter=Q(status='ATENDIDO')),
            ausencias=Count('id', filter=Q(status='FALTOU')),
        )
        .order_by('horario__data')
    )

    dados_por_data = list(agendamentos_por_data)
    context = {
        'dados_por_data': dados_por_data,
        'total_agendados': sum(d['agendados'] for d in dados_por_data),
        'total_atendidos': sum(d['atendidos'] for d in dados_por_data),
        'total_ausencias': sum(d['ausencias'] for d in dados_por_data),
    }
    return render(request, 'login_agendafacil/dados_admin.html', context)

@login_required
def gerenciamento_usuarios(request):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')

    context = {
        'clientes': Usuario.objects.filter(tipo_usuario='CLIENTE').order_by('first_name'),
        'atendentes': Usuario.objects.filter(tipo_usuario='ATENDENTE').order_by('first_name'),
    }
    return render(request, 'login_agendafacil/gerenciamento_usuarios.html', context)

@login_required
def visualizacao_feedback(request):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')

    feedbacks = FeedbackCliente.objects.all().order_by('-criado_em')
    return render(request, 'login_agendafacil/visualizacao_feedback.html', {'feedbacks': feedbacks})

@login_required
def gerenciamento_usuarios(request):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')
    
    usuarios = Usuario.objects.exclude(tipo_usuario='ADMIN')
    
    # 🔹 Criar usuário
    if 'criar_usuario' in request.POST:
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciamento_usuarios')
            
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        acao = request.POST.get('acao')

        usuario = get_object_or_404(Usuario, id=usuario_id)

        ## ativação / desativação
        if acao == 'ativar':
            usuario.is_active = True
            usuario.save()
            messages.success(request, f'Usuário {usuario.CPF} ativado com sucesso!')

        elif acao == 'desativar':
            usuario.is_active = False
            usuario.save()
            messages.success(request, f'Usuário {usuario.CPF} desativado com sucesso!')    

        ## tornar atendente / cliente e vice-versa
        
        elif acao == 'tornar_atendente':
            usuario.tipo_usuario = 'ATENDENTE'
            usuario.save()
            messages.success(request, f'Usuário {usuario.CPF} tornou-se atendente com sucesso!')
        elif acao == 'tornar_cliente':
            usuario.tipo_usuario = 'CLIENTE'
            usuario.save()
            messages.success(request, f'Usuário {usuario.CPF} tornou-se cliente com sucesso!')

        return redirect('gerenciamento_usuarios')
    context = {
        'usuarios': usuarios.order_by('first_name')
        }
    return render(request, 'login_agendafacil/gerenciamento_usuarios.html', context)   

@login_required
def criar_usuario_admin(request):
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADMIN'):
        return redirect('redirect_pos_login')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('gerenciamento_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'login_agendafacil/cadastro_cliente.html', {'form': form})


## PAINÉIS ATENDENTE
@login_required
def painel_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    
    hoje = date.today()
    agendamentos = Agendamento.objects.filter(
        horario__atendente=request.user,
        horario__data=hoje
    ).order_by('horario__horario')
    
    context = {
        'agendamentos': agendamentos,
        'hoje': hoje
    }

    return render(request, 'login_agendafacil/painel_atendente.html', {
        'agendamentos': agendamentos,
        'hoje': hoje,
    })


@login_required
def perfil_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/perfil_atendente.html')


@login_required
def atendimento(request, agendamento_id):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    
    agendamento = get_object_or_404(
        Agendamento, 
        id=agendamento_id,
        atendente=request.user,
        status='CONFIRMADO'
    )
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.agendamento = agendamento
            atendimento.atendente = request.user
            atendimento.save()
            agendamento.status = 'ATENDIDO'
            agendamento.save()
            return redirect('painel_atendente')
    else:
        form = AtendimentoForm()
         
    return render(request, 'login_agendafacil/atendimento.html',{
        'form': form,
        'agendamento': agendamento
    })
@login_required
def lista_atendimentos(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    
    atendimentos = Agendamento.objects.filter(
        horario__atendente=request.user,
        status='AGENDADO'
    ).order_by('horario__data', 'horario__horario')

    return render(request, 'login_agendafacil/lista_atendimentos.html', {
        'atendimentos': atendimentos
    })

@login_required
def dados_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/dados_atendente.html')

@login_required
def editar_perfil_atendente(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_atendente')
    else:
        form = UsuarioUpdateForm(instance=request.user)

    return render(request, 'login_agendafacil/editar_perfil_atendente.html', {'form': form})



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
def editar_perfil_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_cliente')
    else:
        form = UsuarioUpdateForm(instance=request.user)

    return render(request, 'login_agendafacil/editar_perfil_cliente.html', {'form': form})

@login_required
def perfil_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')

    return render(request, 'login_agendafacil/perfil_cliente.html')

@login_required
def feedback_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')

    agendamentos_disponiveis = Agendamento.objects.filter(
        cliente=request.user,
        status='ATENDIDO',
        feedback__isnull=True
    )
    feedbacks_enviados = FeedbackCliente.objects.filter(
        cliente=request.user
        ).select_related('agendamento', 'atendente').order_by('-criado_em')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            
            if feedback.agendamento not in agendamentos_disponiveis:
                messages.error(request, "Agendamento inválido.")
                return redirect('feedback_cliente')
                        
            feedback.cliente = request.user
            feedback.atendente = feedback.agendamento.atendente
            feedback.save()
            messages.success(request, 'Feedback enviado! Obrigado.')
            return redirect('painel_cliente')
    else:
        form = FeedbackForm()

    form.fields['agendamento'].queryset = agendamentos_disponiveis
    return render(request, 'login_agendafacil/feedback_cliente.html', {
        'form': form,
        'agendamentos_disponiveis': agendamentos_disponiveis,
        'feedbacks_enviados': feedbacks_enviados
    })

@login_required
def dados_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/perfil_cliente.html')


## agendamento_cliente
@login_required
def agendamento_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect ('redirect_pos_login')
    
    hoje = date.today()
    data_selecionada = request.GET.get('data') or request.POST.get('data')

    datas = HorarioAtendimento.objects.filter(
       disponivel=True).values_list('data', flat=True).distinct().order_by('data')
    
    horarios = None
    
    if data_selecionada:
        horarios = HorarioAtendimento.objects.filter(
            disponivel=True,
            data=data_selecionada
        ).order_by('horario')

    if request.method == 'POST':
        horarios_id = request.POST.get('horario_id')
        data_selecionada = request.POST.get('data')
        horario = get_object_or_404(
            HorarioAtendimento,
            id=horarios_id, 
            disponivel=True)

        Agendamento.objects.create(
            cliente=request.user,
            horario=horario,
        )
        horario.disponivel = False
        horario.save()

        return redirect('painel_cliente')
    return render(request, 'login_agendafacil/agendamento_cliente.html', {
        'datas': datas,
        'horarios': horarios,
        'data_selecionada': data_selecionada,
        'hoje': hoje
    })


@login_required
def painel_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    
    agendamentos = request.user.agendamentos.all()
    agendamento_id = request.GET.get('agendamento')

    agendados = agendamentos.filter(status='AGENDADO')
    atendidos = agendamentos.filter(status='ATENDIDO')
    cancelados = agendamentos.filter(status='CANCELADO')

    return render(request, 'login_agendafacil/painel_cliente.html', {
        'agendados': agendados,
        'atendidos': atendidos,
        'cancelados': cancelados,
    })


