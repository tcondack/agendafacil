from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UsuarioForm

def index_login(request):
    return render(request, 'login_agendafacil/index_login.html')


def cadastro_cliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
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

    elif request.user.groups.filter(name='Colaborador').exists():
        return redirect('painel_colaborador')

    else:
        return redirect('painel_cliente')


