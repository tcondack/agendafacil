
from django.contrib import admin
from django.urls import path
from app_agenda_facil import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.base, name='base')
]
