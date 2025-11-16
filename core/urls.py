from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
# Rota para a Home Page
path('', views.home, name='home'),

# Rota para a Página de Login
path('login/', auth_views.LoginView.as_view(
    template_name='login.html',
    redirect_authenticated_user=True 
), name='login'),

# (CORRIGIDO) Rota para fazer Logout
# Adicionamos 'next_page="home"' para que o logout via GET funcione
# e redirecione corretamente para a home.
path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


]