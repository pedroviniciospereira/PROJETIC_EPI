# colaboradores/views.py

from django.shortcuts import render, redirect, get_object_or_404 
from .models import Colaborador
from .forms import ColaboradorForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

@login_required 
def colaborador_lista(request):
    query = request.GET.get('q', '')
    
    if query:
        colaboradores = Colaborador.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(matricula__icontains=query) |
            Q(funcao__icontains=query)
        ).order_by('nome_completo')
    else:
        colaboradores = Colaborador.objects.all().order_by('nome_completo')
    
    total_colaboradores = colaboradores.count()
    colaboradores_ativos = colaboradores.filter(status='Ativo').count()
    colaboradores_inativos = total_colaboradores - colaboradores_ativos

    context = {
        'colaboradores_lista': colaboradores,
        'total_colaboradores': total_colaboradores,
        'colaboradores_ativos': colaboradores_ativos,
        'colaboradores_inativos': colaboradores_inativos,
        'search_query': query,
    }
    return render(request, 'index.html', context)


@login_required 
def colaborador_novo(request):
    sugestoes_base = ['Pedreiro', 'Servente', 'Mestre de Obras', 'Carpinteiro', 'Eletricista']
    funcoes_db = Colaborador.objects.values_list('funcao', flat=True).distinct()
    todas_funcoes = sorted(list(set(sugestoes_base) | set(funcoes_db)))

    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            # IMPORTANTE: Usamos redirect para limpar o formulário e processar a mensagem
            return redirect('cadastro') 
    else:
        form = ColaboradorForm() 

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Colaborador',
        'sugestoes_funcoes': todas_funcoes 
    }
    return render(request, 'cadastro.html', context)


@login_required 
def colaborador_editar(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    sugestoes_base = ['Pedreiro', 'Servente', 'Mestre de Obras', 'Carpinteiro', 'Eletricista']
    funcoes_db = Colaborador.objects.values_list('funcao', flat=True).distinct()
    todas_funcoes = sorted(list(set(sugestoes_base) | set(funcoes_db)))

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador alterado com sucesso!')
            # Redirect garante que a mensagem não fique presa
            return redirect('index') 
    else:
        form = ColaboradorForm(instance=colaborador) 

    context = {
        'form': form,
        'colaborador': colaborador,
        'titulo_pagina': 'Editar Colaborador',
        'sugestoes_funcoes': todas_funcoes 
    }
    return render(request, 'cadastro.html', context)


@login_required 
def colaborador_excluir(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        try:
            nome_colaborador = colaborador.nome_completo
            colaborador.delete()
            # Esta é a única mensagem que deve aparecer ao excluir
            messages.success(request, f'Colaborador "{nome_colaborador}" foi excluído.')
        except ProtectedError:
            messages.error(request, f'Erro: O colaborador "{colaborador.nome_completo}" tem empréstimos registrados e não pode ser excluído.')
    
    return redirect('index')