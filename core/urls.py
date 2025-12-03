from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True 
    ), name='login'),

    # Logout Personalizado (Funciona com GET)
    path('logout/', views.custom_logout, name='logout'),
    
    # Perfil
    path('sistema/perfil/', views.perfil, name='perfil'),
    
    # Alterar Senha
    path('sistema/perfil/senha/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        success_url='/sistema/perfil/senha/concluido/'
    ), name='password_change'),
    
    path('sistema/perfil/senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),
]