"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Importa as funcionalidades de administração do Django.
from django.contrib import admin
# Importa as funções 'path' (para definir rotas) e 'include' (para incluir URLs de outros apps).
from django.urls import path, include


# O 'urlpatterns' é a lista padrão que o Django procura para definir as rotas do site.
urlpatterns = [
    # Define a rota para o painel de administração do Django.
    # Qualquer URL que comece com 'admin/' será gerenciada pelo admin.site.urls.
    path('admin/', admin.site.urls),
    
    # (NOVO) Faz o app 'core' controlar a raiz do site (/)
    # Isso vai carregar as rotas 'home', 'login' e 'logout'
    path('', include('core.urls')),
    
    # (EDITADO) Movemos seu sistema de colaboradores para '/sistema/'
    # Agora, a lista de colaboradores será: /sistema/
    # E o cadastro será: /sistema/cadastro/
    path('sistema/', include('colaboradores.urls')),
]