// Função principal que é executada quando o DOM está pronto
document.addEventListener("DOMContentLoaded", function() {
    
    // Tenta configurar a lógica da matrícula (substituindo o CPF)
    setupMatriculaInput();

    // Tenta configurar o menu do usuário (roda em todas as páginas)
    setupUserMenu();
    
    // Tenta configurar o modal de exclusão (nas páginas de lista)
    setupDeleteModal();

    // Tenta configurar o modal de feedback (nas páginas de lista e cadastro)
    setupFeedbackModal();
    
    // (NOVO) Tenta configurar o formulário de "carrinho" (só na pág. novo_emprestimo)
    setupEmprestimoFormset();

    // (NOVO) Renderiza todos os ícones Feather Icons (ex: <svg class="icon">)
    // Garante que a biblioteca 'feather' foi carregada
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});

/**
 * Procura pelo campo MATRICULA e força a aceitar apenas números
 */
function setupMatriculaInput() {
    // Usamos o ID que definimos no forms.py
    const matriculaInput = document.getElementById("matricula"); 
    
    if (matriculaInput) {
        matriculaInput.addEventListener('input', function(e) {
            // Remove qualquer coisa que não seja um dígito
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }
}

/**
 * Configura o menu dropdown do usuário na sidebar
 */
function setupUserMenu() {
    const menuTrigger = document.getElementById("user-menu-trigger");
    const userMenu = document.getElementById("user-menu");

    if (menuTrigger && userMenu) {
        
        // 1. Abre/Fecha o menu ao clicar no gatilho
        menuTrigger.addEventListener("click", function(event) {
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
        });

        // 2. Fecha o menu se clicar fora
        window.addEventListener("click", function(event) {
            if (userMenu.classList.contains("show") && !userMenu.contains(event.target)) {
                userMenu.classList.remove("show");
            }
        });
    }
}


/**
 * Configura os gatilhos e ações do modal de exclusão
 * (Funciona para Colaboradores e Equipamentos)
 */
function setupDeleteModal() {
    const modal = document.getElementById('deleteModal');
    const backdrop = document.getElementById('deleteModalBackdrop');
    const deleteForm = document.getElementById('deleteModalForm');
    const collaboratorNameEl = document.getElementById('deleteModalColaboradorNome');
    const closeBtn = document.getElementById('closeModalBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');
    const deleteTriggers = document.querySelectorAll('.delete-trigger'); // Pega TODOS os botões de excluir

    if (!modal || !deleteTriggers.length || !backdrop || !deleteForm) {
        return; // Não está em uma página de lista, então pare
    }

    const openModal = (url, nome) => {
        deleteForm.action = url; 
        collaboratorNameEl.textContent = nome; 
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    };

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
    };

    deleteTriggers.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault(); 
            const url = this.href;
            const nome = this.getAttribute('data-nome');
            openModal(url, nome);
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);
}


/**
 * Verifica se há mensagens de feedback (sucesso ou erro)
 * e exibe o modal. (Funciona em qualquer página que tenha o modal)
 */
function setupFeedbackModal() {
    const dataDiv = document.getElementById('feedbackData');
    const modal = document.getElementById('feedbackModal');
    const backdrop = document.getElementById('feedbackModalBackdrop');
    const header = document.getElementById('feedbackModalHeader');
    const title = document.getElementById('feedbackModalTitle');
    const body = document.getElementById('feedbackModalBody');
    const closeBtn = document.getElementById('feedbackModalCloseBtn');
    const okBtn = document.getElementById('feedbackModalOkBtn');

    if (!dataDiv || !modal || !backdrop) {
        return; // Não está em uma página com modal de feedback
    }

    // Pega as mensagens dos atributos data-*
    // (O 'trim()' remove espaços em branco)
    const successMessage = dataDiv.dataset.successMessage ? dataDiv.dataset.successMessage.trim() : "";
    const errorMessage = dataDiv.dataset.errorMessage ? dataDiv.dataset.errorMessage.trim() : "";

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
        header.classList.remove('modal-header-success', 'modal-header-danger');
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (okBtn) okBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // Verifica se há mensagem de SUCESSO
    if (successMessage) {
        title.textContent = 'Sucesso!';
        // (ALTERADO) Usa innerHTML para processar tags <br> se houver múltiplas mensagens
        body.innerHTML = successMessage; 
        header.classList.add('modal-header-success');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    } 
    // Senão, verifica se há mensagem de ERRO
    else if (errorMessage) {
        title.textContent = 'Falha';
        // (ALTERADO) Usa innerHTML para processar tags <br>
        body.innerHTML = errorMessage; 
        header.classList.add('modal-header-danger');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    }
}

/**
 * (NOVO) Configura a lógica de adicionar/remover
 * formulários no "carrinho" da página de Novo Empréstimo.
 */
function setupEmprestimoFormset() {
    const container = document.getElementById('item-forms-container');
    const addButton = document.getElementById('add-item-btn');
    const template = document.getElementById('empty-form-template');
    const totalFormsInput = document.getElementById('id_itens-TOTAL_FORMS');

    // Se não estamos na página 'novo_emprestimo.html', saia da função
    if (!container || !addButton || !template || !totalFormsInput) {
        return;
    }

    // Pega o número atual de formulários
    let formCount = parseInt(totalFormsInput.value, 10);

    addButton.addEventListener('click', function() {
        // Clona o template
        // Substitui o prefixo '__prefix__' pelo número do novo formulário
        const newFormHtml = template.innerHTML.replace(/__prefix__/g, formCount);
        const newElement = document.createElement('div');
        newElement.innerHTML = newFormHtml;
        
        // Adiciona o novo formulário ao container
        container.appendChild(newElement.firstElementChild); // Adiciona o .item-form-container
        
        // Incrementa o contador total de formulários
        formCount++;
        totalFormsInput.value = formCount;
    });
}