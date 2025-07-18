from django.shortcuts import render

def index(request):
    return render(request, 'usuarios/index.html')

def perfil(request):
    return render(request, 'usuarios/perfil.html')

def adm_perfil(request):
    return render (request, 'usuarios/adm_perfil')




