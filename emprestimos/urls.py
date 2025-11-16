from django.urls import path
from . import views

# Rotas do app 'emprestimos'
urlpatterns = [
    # Rota para a lista de empréstimos
    # ex: /sistema/emprestimos/
    path('', views.lista_emprestimo, name='lista_emprestimo'),
    
    # Rota para o formulário de novo empréstimo
    # ex: /sistema/emprestimos/novo/
    path('novo/', views.novo_emprestimo, name='novo_emprestimo'),
    
    # Rota para ver os detalhes de um empréstimo
    # ex: /sistema/emprestimos/detalhe/5/
    path('detalhe/<int:id>/', views.detalhe_emprestimo, name='detalhe_emprestimo'),
    
    # (ATUALIZADO) Rota para processar a devolução PARCIAL de um item
    # ex: /sistema/emprestimos/devolver-parcial/22/ (onde 22 é o ID do *ItemEmprestado*)
    path('devolver-parcial/<int:item_id>/', views.devolver_item_parcial, name='devolver_item_parcial'),
]