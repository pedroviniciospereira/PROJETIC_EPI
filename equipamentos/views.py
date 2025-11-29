from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Equipamento
from .forms import EquipamentoForm
from django.db.models import ProtectedError

# Create your views here.

@login_required
def equipamento_lista(request):
    ##
    ## View para listar todos os equipamentos com filtro de busca.
    ##
    query = request.GET.get('q', '')
    
    if query:
        # Busca por nome, C.A. ou categoria
        equipamentos = Equipamento.objects.filter(
            Q(nome__icontains=query) |
            Q(ca__icontains=query) |
            Q(categoria__icontains=query)
        ).order_by('nome')
    else:
        equipamentos = Equipamento.objects.all().order_by('nome')

    context = {
        'equipamentos_lista': equipamentos,
        'search_query': query,
        # (CORRIGIDO) A linha 'messages' foi removida daqui
    }
    # Aponta para o template na raiz
    return render(request, 'equipamento_lista.html', context)


@login_required
def equipamento_novo(request):
    ##
    ## View para cadastrar um novo equipamento.
    ##
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            
            # (CORREÇÃO) Em vez de redirecionar, vamos 
            # renderizar a página novamente com um form vazio
            # e uma flag de sucesso para o modal.
            form_vazio = EquipamentoForm()
            context = {
                'form': form_vazio,
                'titulo_pagina': 'Cadastrar Novo Equipamento',
                'cadastro_sucesso': True # Flag para o modal
            }
            return render(request, 'equipamento_form.html', context)
    else:
        form = EquipamentoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Equipamento'
    }
    # Aponta para o template na raiz
    return render(request, 'equipamento_form.html', context)


@login_required
def equipamento_editar(request, id):
    ##
    ## View para editar um equipamento existente.
    ##
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('equipamento_lista')
    else:
        # Cria o formulário pré-preenchido com os dados do equipamento
        form = EquipamentoForm(instance=equipamento)

    context = {
        'form': form,
        'equipamento': equipamento, # Passa o objeto para o template
        'titulo_pagina': 'Editar Equipamento'
    }
    # Aponta para o template na raiz
    return render(request, 'equipamento_form.html', context)


@login_required
def equipamento_excluir(request, id):
    ##
    ## View para excluir um equipamento (via POST, do modal).
    ##
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        ##
        ## VERIFICAÇÃO DE SEGURANÇA:
        ## Só permite excluir se o estoque disponível for igual ao total
        ## (ou seja, nenhum item está emprestado)
        ##
        if equipamento.estoque_disponivel < equipamento.estoque_total:
            messages.error(request, f'ERRO: O equipamento "{equipamento.nome}" não pode ser excluído pois há itens emprestados.')
        else:
            nome_equipamento = equipamento.nome
            equipamento.delete()
            messages.success(request, f'Equipamento "{nome_equipamento}" foi excluído com sucesso.')
    
    # Redireciona de volta para a lista em qualquer caso
    return redirect('equipamento_lista')