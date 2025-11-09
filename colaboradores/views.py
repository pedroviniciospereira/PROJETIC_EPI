# Importações necessárias do Django
# ================================
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Colaborador
# (EDITADO) Importa o ColaboradorForm que você criou
from .forms import ColaboradorForm
from django.db.models import Q
from django.contrib import messages
# (NOVO) Importa o "segurança" que tranca a view
from django.contrib.auth.decorators import login_required

# View (Função) para a página de LISTA de Colaboradores (index.html)
# =================================================================
@login_required # (NOVO) Tranca esta view
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

    # Passa as mensagens (para o modal de feedback de Edição/Exclusão)
    context = {
        'colaboradores_lista': colaboradores,
        'total_colaboradores': total_colaboradores,
        'colaboradores_ativos': colaboradores_ativos,
        'colaboradores_inativos': colaboradores_inativos,
        'search_query': query,
        'messages': messages.get_messages(request) # Passa as mensagens para o template
    }
    return render(request, 'index.html', context)


# View (Função) para a página de CADASTRO de Colaboradores (cadastro.html)
# ======================================================================
@login_required # (NOVO) Tranca esta view
def colaborador_novo(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid(): # O form.is_valid() chama o clean_matricula
            form.save()
            
            # Prepara um novo form vazio e envia a flag de sucesso
            form_vazio = ColaboradorForm()
            return render(request, 'cadastro.html', {
                'form': form_vazio,
                'cadastro_sucesso': True # Para o seu modal de sucesso
            })
        # Se for inválido, o form com os erros é passado abaixo
    else:
        form = ColaboradorForm() # Cria um form vazio

    # O 'form' (com erros ou vazio) é enviado para o template
    return render(request, 'cadastro.html', {'form': form})


# View (Função) para a página de EDIÇÃO de Colaboradores (reutiliza cadastro.html)
# ==============================================================================
@login_required # (NOVO) Tranca esta view
def colaborador_editar(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador alterado com sucesso!')
            return redirect('index') # Redireciona para a lista
    else:
        form = ColaboradorForm(instance=colaborador) # Pré-preenche

    context = {
        'form': form,
        'colaborador': colaborador
    }
    return render(request, 'cadastro.html', context)


# View (Função) para EXCLUIR um Colaborador
# =========================================
@login_required # (NOVO) Tranca esta view
def colaborador_excluir(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    # Adiciona verificação de POST para segurança do modal
    if request.method == 'POST':
        nome_colaborador = colaborador.nome_completo
        colaborador.delete()
        messages.success(request, f'Colaborador "{nome_colaborador}" foi excluído.')
    
    # Redireciona de volta para a lista em qualquer caso
    return redirect('index')