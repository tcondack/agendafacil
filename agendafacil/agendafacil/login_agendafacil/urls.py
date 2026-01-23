from django.urls import path
from .views import cadastro_cliente, index_login
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', index_login, name='index_login'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('login_cliente/', auth_views.LoginView.as_view(template_name='login_agendafacil/login_cliente.html'), name='login_cliente'),
    path('login_colaborador/', auth_views.LoginView.as_view(template_name='login_agendafacil/login_colaborador.html'), name='login_colaborador'),
    path('login_admin/', auth_views.LoginView.as_view(template_name='login_agendafacil/login_admin.html'), name='login_admin'),
]
