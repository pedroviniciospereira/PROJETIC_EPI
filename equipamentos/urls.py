from django.urls import path
from . import views

# Rotas do app 'equipamentos'
urlpatterns = [
    # Rota para a lista de equipamentos
    # ex: /sistema/equipamentos/
    path('', views.equipamento_lista, name='equipamento_lista'),
    
    # Rota para o formulário de cadastro de novo equipamento
    # ex: /sistema/equipamentos/novo/
    path('novo/', views.equipamento_novo, name='equipamento_novo'),
    
    # Rota para editar um equipamento específico
    # ex: /sistema/equipamentos/editar/5/ (onde 5 é o ID do equipamento)
    path('editar/<int:id>/', views.equipamento_editar, name='equipamento_editar'),
    
    # Rota para excluir um equipamento específico (será chamada pelo modal)
    # ex: /sistema/equipamentos/excluir/5/
    path('excluir/<int:id>/', views.equipamento_excluir, name='equipamento_excluir'),
]