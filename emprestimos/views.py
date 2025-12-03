# emprestimos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction 
from django.db.models import Q
from django.utils import timezone
from .models import Emprestimo, ItemEmprestado, HistoricoDevolucao
from .forms import EmprestimoForm, ItemEmprestadoFormSet, DevolucaoParcialForm
# Importação necessária para corrigir erros no Codespace
from django.views.decorators.csrf import csrf_exempt 

@login_required
def lista_emprestimo(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    emprestimos = Emprestimo.objects.select_related('colaborador').all().order_by('-data_emprestimo')

    if query:
        emprestimos = emprestimos.filter(
            Q(colaborador__nome_completo__icontains=query) |
            Q(id__icontains=query) |
            Q(itens_emprestados__equipamento__nome__icontains=query) 
        ).distinct()

    if status_filter:
        emprestimos = emprestimos.filter(status=status_filter)
        
    hoje = timezone.now().date()
    Emprestimo.objects.filter(
        status='ATIVO', 
        data_prevista_devolucao__lt=hoje
    ).update(status='ATRASADO')
    
    kpi_ativos = Emprestimo.objects.filter(status='ATIVO').count()
    kpi_atrasados = Emprestimo.objects.filter(status='ATRASADO').count()
    kpi_devolvidos = Emprestimo.objects.filter(status='DEVOLVIDO').count()

    context = {
        'lista_emprestimos': emprestimos,
        'search_query': query,
        'status_filter': status_filter,
        'kpi_ativos': kpi_ativos,
        'kpi_atrasados': kpi_atrasados,
        'kpi_devolvidos': kpi_devolvidos,
    }
    return render(request, 'lista_emprestimo.html', context)


@csrf_exempt # <--- CORREÇÃO APLICADA AQUI
@login_required
@transaction.atomic 
def novo_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        formset = ItemEmprestadoFormSet(request.POST, prefix='itens')

        if form.is_valid() and formset.is_valid():
            emprestimo = form.save()
            itens = formset.save(commit=False)
            
            equipamentos_no_carrinho = []

            for item in itens:
                # Validação: Item duplicado
                if item.equipamento in equipamentos_no_carrinho:
                    messages.error(request, f"Erro: O equipamento '{item.equipamento.nome}' foi adicionado mais de uma vez.")
                    return render(request, 'novo_emprestimo.html', {'form': form, 'formset': formset, 'titulo_pagina': 'Novo Empréstimo'})
                
                equipamentos_no_carrinho.append(item.equipamento)
                equipamento = item.equipamento
                
                # Validação: Estoque
                if item.quantidade_emprestada > equipamento.estoque_disponivel:
                    messages.error(request, f"Erro no estoque de '{equipamento.nome}'. Disponível: {equipamento.estoque_disponivel}")
                    return render(request, 'novo_emprestimo.html', {'form': form, 'formset': formset, 'titulo_pagina': 'Novo Empréstimo'})
                
                # Baixa no estoque
                equipamento.estoque_disponivel -= item.quantidade_emprestada
                equipamento.save()
                
                item.emprestimo = emprestimo
                item.save()

            messages.success(request, f"Empréstimo #{emprestimo.id} registrado com sucesso!")
            return redirect('novo_emprestimo')
        else:
            messages.error(request, "Formulário inválido. Verifique os erros abaixo.")

    else:
        form = EmprestimoForm()
        formset = ItemEmprestadoFormSet(prefix='itens', queryset=ItemEmprestado.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'titulo_pagina': 'Novo Empréstimo'
    }
    return render(request, 'novo_emprestimo.html', context)
    

@login_required
def detalhe_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo.objects.prefetch_related('itens_emprestados__equipamento'), id=id)
    
    itens_emprestados = emprestimo.itens_emprestados.prefetch_related('historico_devolucoes').all()
    
    itens_com_contexto = []
    for item in itens_emprestados:
        form_devolucao = None
        historico_item = item.historico_devolucoes.all().order_by('-data_devolucao')
        
        if item.status_item == 'PENDENTE':
            form_devolucao = DevolucaoParcialForm(
                prefix=f'item_{item.id}',
                item_emprestado_instance=item
            )

        itens_com_contexto.append((item, form_devolucao, historico_item))

    context = {
        'emprestimo': emprestimo,
        'itens_com_contexto': itens_com_contexto, 
    }
    return render(request, 'detalhe_emprestimo.html', context)


@csrf_exempt # <--- CORREÇÃO APLICADA AQUI TAMBÉM
@login_required
@transaction.atomic
def devolver_item_parcial(request, item_id):
    if request.method != 'POST':
        return redirect('lista_emprestimo') 

    item = get_object_or_404(ItemEmprestado, id=item_id)
    form = DevolucaoParcialForm(request.POST, prefix=f'item_{item.id}', item_emprestado_instance=item)

    if form.is_valid():
        nova_devolucao = form.save(commit=False)
        nova_devolucao.item_emprestado = item
        nova_devolucao.save()

        equipamento = item.equipamento
        status = nova_devolucao.status_devolucao
        qtd_devolvida = nova_devolucao.quantidade_devolvida
        
        if status in ['DEVOLVIDO', 'DANIFICADO']:
            equipamento.estoque_disponivel += qtd_devolvida
            equipamento.save()
            messages.success(request, f"'{equipamento.nome}' (Qtde: {qtd_devolvida}) devolvido ao estoque.")
        
        elif status == 'PERDIDO':
            messages.warning(request, f"'{equipamento.nome}' (Qtde: {qtd_devolvida}) registrado como Perdido.")

        if item.get_quantidade_pendente() == 0:
            item.status_item = 'CONCLUIDO'
            item.save()

        emprestimo = item.emprestimo
        status_dos_itens = emprestimo.itens_emprestados.values_list('status_item', flat=True)
        
        if 'PENDENTE' not in status_dos_itens:
            emprestimo.status = 'DEVOLVIDO' 
            emprestimo.save()
            messages.info(request, f"Todos os itens do Empréstimo #{emprestimo.id} foram processados. Empréstimo concluído.")

    else:
        # Recupera erro de forma segura
        erro = list(form.errors.values())[0][0] if form.errors else "Erro ao processar formulário."
        messages.error(request, f"Erro ao processar devolução: {erro}")

    return redirect('detalhe_emprestimo', id=item.emprestimo.id)