from django.urls import path
from .views import cadastro_cliente, index_login, redirect_pos_login
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', index_login, name='index_login'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login_agendafacil/login.html'), name='login'),
    path('pos_login/', redirect_pos_login, name='redirect_pos_login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
]
