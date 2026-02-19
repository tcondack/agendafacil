from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index_login, redirect_pos_login, cadastro_cliente, painel_admin, painel_atendente, painel_cliente, perfil_atendente, atendimento_atendente, dados_atendente
from . import views

urlpatterns =[
    path('', index_login, name='index_login'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login_agendafacil/login.html'), name='login'),
   
    path('pos-login/', redirect_pos_login, name='redirect_pos_login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('painel_admin/', painel_admin, name='painel_admin'),

    ## sessão atendente 
    path('painel_atendente/', painel_atendente, name='painel_atendente'),
    path('perfil_atendente/', perfil_atendente, name='perfil_atendente'),
    path('atendimento_atendente/', atendimento_atendente, name='atendimento_atendente'),
    path('dados_atendente/', dados_atendente, name='dados_atendente'),
    path('alterar_status/<int:agendamento_id>/<str:status>/', views.alterar_status,name='alterar_status'),

    ## sessão cliente
    path('painel_cliente/', painel_cliente, name='painel_cliente'),
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('agendamento_cliente/', views.agendamento_cliente, name='agendamento_cliente'),
    path('feedback_cliente/<int:agendamento_id>/', views.feedback_cliente, name='feedback_cliente'),
    path('dados_cliente/', views.dados_cliente, name='dados_cliente'),
]
