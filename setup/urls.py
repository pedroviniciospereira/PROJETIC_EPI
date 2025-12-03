from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importação necessária
from django.conf.urls.static import static # Importação necessária para arquivos de mídia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('sistema/', include('colaboradores.urls')),
    path('sistema/equipamentos/', include('equipamentos.urls')),
    path('sistema/emprestimos/', include('emprestimos.urls')),
]

# Adiciona suporte a arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)