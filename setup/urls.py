"""
URL configuration for setup project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # O Admin do Django (para criar usuários)
    path('admin/', admin.site.urls),
    
    # Rotas públicas (Home, Login, Logout)
    path('', include('core.urls')),
    
    # Rotas do sistema de Colaboradores
    path('sistema/', include('colaboradores.urls')),
    
    # Rotas do sistema de Equipamentos
    path('sistema/equipamentos/', include('equipamentos.urls')),
    
    # (NOVO) Rotas do sistema de Empréstimos
    # (ex: /sistema/emprestimos/novo/)
    path('sistema/emprestimos/', include('emprestimos.urls')),
]

# Adiciona suporte a arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)