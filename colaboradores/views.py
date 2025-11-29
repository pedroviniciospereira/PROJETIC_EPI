# Importações necessárias do Django
# ================================
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Colaborador
from .forms import ColaboradorForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

# View (Função) para a página de LISTA de Colaboradores (index.html)
# =================================================================
@login_required 
def colaborador_lista(request):
    query = request.GET.get('q', '')
    
    if query:
        colaboradores = Colaborador.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(matricula__icontains=query) |
            Q(funcao__icontains=query)
        ).order_by('-data_cadastro')
    else:
        colaboradores = Colaborador.objects.all().order_by('-data_cadastro')
    
    total_colaboradores = colaboradores.count()
    colaboradores_ativos = colaboradores.filter(status='Ativo').count()
    colaboradores_inativos = total_colaboradores - colaboradores_ativos

    context = {
        'colaboradores_lista': colaboradores,
        'total_colaboradores': total_colaboradores,
        'colaboradores_ativos': colaboradores_ativos,
        'colaboradores_inativos': colaboradores_inativos,
        'search_query': query,
        # (CORRIGIDO) A linha 'messages' foi removida daqui
    }
    return render(request, 'index.html', context)


# View (Função) para a página de CADASTRO de Colaboradores (cadastro.html)
# ======================================================================
@login_required 
def colaborador_novo(request):
    # 1. Definir suas sugestões base (fixas)
    sugestoes_base = ['Pedreiro', 'Servente', 'Mestre de Obras', 'Carpinteiro', 'Eletricista']
    
    # 2. Buscar funções que já existem no banco de dados (dinâmicas)
    # .values_list('funcao', flat=True) pega apenas o texto da coluna 'funcao'
    # .distinct() garante que não venham nomes repetidos
    funcoes_db = Colaborador.objects.values_list('funcao', flat=True).distinct()
    
    # 3. Unir as duas listas e remover duplicatas usando set(), depois ordenar
    todas_funcoes = sorted(list(set(sugestoes_base) | set(funcoes_db)))

    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            form_vazio = ColaboradorForm()
            return render(request, 'cadastro.html', {
                'form': form_vazio,
                'titulo_pagina': 'Cadastrar Novo Colaborador',
                'cadastro_sucesso': True,
                'sugestoes_funcoes': todas_funcoes # <--- Passar para o template
            })
    else:
        form = ColaboradorForm() 

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Colaborador',
        'sugestoes_funcoes': todas_funcoes # <--- Passar para o template
    }
    return render(request, 'cadastro.html', context)


# View (Função) para a página de EDIÇÃO de Colaboradores (reutiliza cadastro.html)
# ==============================================================================
@login_required 
def colaborador_editar(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    # --- Repetir a lógica de sugestões aqui ---
    sugestoes_base = ['Pedreiro', 'Servente', 'Mestre de Obras', 'Carpinteiro', 'Eletricista']
    funcoes_db = Colaborador.objects.values_list('funcao', flat=True).distinct()
    todas_funcoes = sorted(list(set(sugestoes_base) | set(funcoes_db)))
    # ------------------------------------------

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador alterado com sucesso!')
            return redirect('index') 
    else:
        form = ColaboradorForm(instance=colaborador) 

    context = {
        'form': form,
        'colaborador': colaborador,
        'titulo_pagina': 'Editar Colaborador',
        'sugestoes_funcoes': todas_funcoes # <--- Passar para o template
    }
    return render(request, 'cadastro.html', context)


# View para EXCLUIR um Colaborador
@login_required 
def colaborador_excluir(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        try:
            nome_colaborador = colaborador.nome_completo
            colaborador.delete()
            messages.success(request, f'Colaborador "{nome_colaborador}" foi excluído.')
        except ProtectedError:
            # Se der erro de proteção (tem empréstimos), mostra esta mensagem
            messages.error(request, f'Erro: O colaborador "{colaborador.nome_completo}" tem empréstimos registrados e não pode ser excluído.')
    
    return redirect('index')