from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UsuarioForm
from .models import Usuario, agendamento


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
        return redirect('painel_colaborador')

    elif request.user.tipo_usuario == 'CLIENTE':
        return redirect('painel_cliente')

    else:
        return redirect('painel_cliente')
    

    ## Paines de acordo com o tipo de usuário

##paineis admin    
@login_required
def painel_admin(request):
    return render(request, 'login_agendafacil/painel_admin.html')
@login_required
def dados_admin(request):
    return render(request, 'login_agendafacil/dados_admin.html')
@login_required
def gerenciamento_usuarios(request):
    return render(request, 'login_agendafacil/gerenciamento_usuarios.html')

##paineis colaborador
@login_required
def painel_colaborador(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/painel_colaborador.html')
@login_required
def perfil_colaborador(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/perfil_colaborador.html')
@login_required
def atendimento_colaborador(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/atendimento_colaborador.html')
@login_required
def dados_colaborador(request):
    if request.user.tipo_usuario != 'ATENDENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/dados_colaborador.html')


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
    return render(request, 'login_agendafacil/perfil_cliente.html')
@login_required
def agendamento_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/agendamento_cliente.html')
@login_required
def feedback_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    return render(request, 'login_agendafacil/feedback_cliente.html')   
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

        agendamento.objects.create(
            cliente=request.user,
            data=data,
            horario=horario
        )
        return redirect('perfil_cliente')
    return render(request, 'login_agendafacil/agendamento_cliente.html')

##
@login_required
def painel_cliente(request):
    if request.user.tipo_usuario != 'CLIENTE':
        return redirect('redirect_pos_login')
    
    agendamentos = agendamento.objects.filter(cliente=request.user
    ).order_by('data', 'horario')
    return render(request, 'login_agendafacil/painel_cliente.html', {'agendamentos': agendamentos})
    
