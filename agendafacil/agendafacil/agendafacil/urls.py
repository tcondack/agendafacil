
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Appp principal
    path('', include('app_agenda_facil.urls')),
    
    # App login/cadastro
    path('login/', include('login_agendafacil.urls'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)