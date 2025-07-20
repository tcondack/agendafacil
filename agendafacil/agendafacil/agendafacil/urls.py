
from django.contrib import admin
from django.urls import path
from app_agenda_facil import views
from django.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.index, name='base'),
    path('perfil', views.perfil, name='perfil')
    path('adm_perfil', views.adm_perfil, name='adm_perfil')

]
