from django import views
from django.urls import path
from .views import cadastro_cliente, index_login, redirect_pos_login
from django.contrib.auth import views as auth_views
from .views import painel_admin, painel_colaborador, painel_cliente
from . import views

urlpatterns =[
    path('', index_login, name='index_login'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login_agendafacil/login.html'), name='login'),
   
    path('pos-login/', redirect_pos_login, name='redirect_pos_login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('painel_admin/', painel_admin, name='painel_admin'),
    path('painel_colaborador/',painel_colaborador, name='painel_colaborador'),
    path('painel_cliente/', painel_cliente, name='painel_cliente'),

    ## sessão colaborador
    path('perfil_colaborador/', painel_colaborador, name='perfil_colaborador'),
    path('atendimento_colaborador/', painel_colaborador, name='atendimento_colaborador'),

    ## sessão cliente
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('agendamento_cliente/', views.agendamento_cliente, name='agendamento_cliente'),
    path('feedback_cliente/', views.feedback_cliente, name='feedback_cliente'),
    path('dados_cliente/', views.dados_cliente, name='dados_cliente'),
]
