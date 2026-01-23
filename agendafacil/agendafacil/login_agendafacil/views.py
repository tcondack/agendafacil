from django.shortcuts import redirect, render
from .forms import UsuarioForm

def cadastro_cliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login_cliente')  # Redireciona para a página de login após o cadastro bem-sucedido
    else:
        form = UsuarioForm()
    return render(request, 'login_agendafacil/cadastro_cliente.html', {'form': form})

def index_login(request):
    return render(request, 'login_agendafacil/index_login.html')

def painel_colaborador(request):
    return render(request, 'login_agendafacil/painel_colaborador.html')


def painel_admin(request):
    return render(request, 'login_agendafacil/painel_admin.html')