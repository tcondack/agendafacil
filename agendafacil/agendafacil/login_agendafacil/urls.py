from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index_login, criar_horario_atendimento, redirect_pos_login, cadastro_cliente, atendimento, lista_atendimentos, painel_admin, editar_perfil_cliente, editar_perfil_atendente, painel_atendente, painel_cliente, perfil_atendente, feedback_cliente, dados_atendente
from . import views

urlpatterns =[
    path('', index_login, name='index_login'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login_agendafacil/login.html'), name='login'),
   
    path('pos-login/', redirect_pos_login, name='redirect_pos_login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    
    ## sessão admin
    path('painel_admin/', painel_admin, name='painel_admin'),
    path('gerenciamento-usuarios/', views.gerenciamento_usuarios, name='gerenciamento_usuarios'),
    path('criar-horario-atendimento/', views.criar_horario_atendimento, name='criar_horario_atendimento'),
    path('visualizar-feedbacks/', views.visualizar_feedbacks, name='visualizar_feedbacks'),
    path(),
    ## sessão atendente 
    path('painel_atendente/', painel_atendente, name='painel_atendente'),
    path('perfil_atendente/', perfil_atendente, name='perfil_atendente'),
    path('editar_perfil_atendente/', views.editar_perfil_atendente, name='editar_perfil_atendente'),
    path('lista_atendimento/', views.lista_atendimentos, name='lista_atendimentos'),
    path('atendimento/<int:agendamento_id>/', views.atendimento, name='atendimento'),
    path('dados_atendente/', dados_atendente, name='dados_atendente'),
    path('alterar_status/<int:agendamento_id>/<str:status>/', views.alterar_status,name='alterar_status'),

    ## sessão cliente
    path('painel_cliente/', painel_cliente, name='painel_cliente'),
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('cliente/editar-perfil/', views.editar_perfil_cliente, name='editar_perfil_cliente'),
    path('agendamento_cliente/', views.agendamento_cliente, name='agendamento_cliente'),
    path('feedback_cliente/', views.feedback_cliente, name='feedback_cliente'),
    path('dados_cliente/', views.dados_cliente, name='dados_cliente'),
]
