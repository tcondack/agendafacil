
from django.contrib import admin
from django.urls import path
from app_agenda_facil import views
from django.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', views.perfil, name='perfil'),
    path('', include(admin.site.urls)),
    path('', views.adm_perfil, name='adm_perfil')

]
