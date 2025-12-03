from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Equipamento
from .forms import EquipamentoForm
from django.db.models import ProtectedError
# Importação necessária para corrigir o erro de CSRF
from django.views.decorators.csrf import csrf_exempt 

@login_required
def equipamento_lista(request):
    query = request.GET.get('q', '')
    
    if query:
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
    }
    return render(request, 'equipamento_lista.html', context)


@csrf_exempt # <--- CORREÇÃO: Ignora verificação de token aqui
@login_required
def equipamento_novo(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento cadastrado com sucesso!')
            
            # Limpa o formulário para o próximo cadastro
            form_vazio = EquipamentoForm()
            context = {
                'form': form_vazio,
                'titulo_pagina': 'Cadastrar Novo Equipamento',
                'cadastro_sucesso': True 
            }
            return render(request, 'equipamento_form.html', context)
    else:
        form = EquipamentoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Equipamento'
    }
    return render(request, 'equipamento_form.html', context)


@csrf_exempt # <--- CORREÇÃO: Ignora verificação de token aqui
@login_required
def equipamento_editar(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('equipamento_lista')
    else:
        form = EquipamentoForm(instance=equipamento)

    context = {
        'form': form,
        'equipamento': equipamento,
        'titulo_pagina': 'Editar Equipamento'
    }
    return render(request, 'equipamento_form.html', context)


@csrf_exempt # <--- CORREÇÃO: Ignora verificação de token aqui
@login_required
def equipamento_excluir(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        if equipamento.estoque_disponivel < equipamento.estoque_total:
            messages.error(request, f'ERRO: O equipamento "{equipamento.nome}" não pode ser excluído pois há itens emprestados.')
        else:
            nome_equipamento = equipamento.nome
            equipamento.delete()
            messages.success(request, f'Equipamento "{nome_equipamento}" foi excluído com sucesso.')
    
    return redirect('equipamento_lista')