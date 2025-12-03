// Função principal que é executada quando o DOM está pronto
document.addEventListener("DOMContentLoaded", function() {
    
    setupMatriculaInput();
    setupUserMenu();
    setupDeleteModal();
    setupFeedbackModal(); // Nossa correção está aqui
    setupEmprestimoFormset();

    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});

function setupMatriculaInput() {
    const matriculaInput = document.getElementById("matricula"); 
    if (matriculaInput) {
        matriculaInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }
}

function setupUserMenu() {
    const menuTrigger = document.getElementById("user-menu-trigger");
    const userMenu = document.getElementById("user-menu");

    if (menuTrigger && userMenu) {
        menuTrigger.addEventListener("click", function(event) {
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
        });
        window.addEventListener("click", function(event) {
            if (userMenu.classList.contains("show") && !userMenu.contains(event.target)) {
                userMenu.classList.remove("show");
            }
        });
    }
}

function setupDeleteModal() {
    const modal = document.getElementById('deleteModal');
    const backdrop = document.getElementById('deleteModalBackdrop');
    const deleteForm = document.getElementById('deleteModalForm');
    const collaboratorNameEl = document.getElementById('deleteModalColaboradorNome');
    const closeBtn = document.getElementById('closeModalBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');
    const deleteTriggers = document.querySelectorAll('.delete-trigger'); 

    if (!modal || !deleteTriggers.length || !backdrop || !deleteForm) {
        return; 
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
 * CORREÇÃO PRINCIPAL DO MODAL DE FEEDBACK
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
        return; 
    }

    // Pega as mensagens e remove espaços vazios das pontas
    let successMessage = dataDiv.dataset.successMessage ? dataDiv.dataset.successMessage.trim() : "";
    let errorMessage = dataDiv.dataset.errorMessage ? dataDiv.dataset.errorMessage.trim() : "";

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
        header.classList.remove('modal-header-success', 'modal-header-danger');
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (okBtn) okBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // LÓGICA DE PROTEÇÃO: Só abre se tiver texto real (tamanho > 0)
    if (successMessage.length > 0) {
        title.textContent = 'Sucesso!';
        body.innerHTML = successMessage;
        header.classList.add('modal-header-success');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
        
        // Limpa o conteúdo para não repetir se o JS rodar de novo
        dataDiv.dataset.successMessage = ""; 
    } 
    else if (errorMessage.length > 0) {
        title.textContent = 'Atenção';
        body.innerHTML = errorMessage;
        header.classList.add('modal-header-danger');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
        
        // Limpa o conteúdo
        dataDiv.dataset.errorMessage = "";
    }
    
    // Remove o elemento do DOM para garantir que não será lido novamente
    if(successMessage.length > 0 || errorMessage.length > 0) {
        dataDiv.remove();
    }
}

function setupEmprestimoFormset() {
    const container = document.getElementById('item-forms-container');
    const addButton = document.getElementById('add-item-btn');
    const template = document.getElementById('empty-form-template');
    const totalFormsInput = document.getElementById('id_itens-TOTAL_FORMS');

    if (!container || !addButton || !template || !totalFormsInput) {
        return;
    }

    let formCount = parseInt(totalFormsInput.value, 10);

    addButton.addEventListener('click', function() {
        const newFormHtml = template.innerHTML.replace(/__prefix__/g, formCount);
        const newElement = document.createElement('div');
        newElement.innerHTML = newFormHtml;
        container.appendChild(newElement.firstElementChild); 
        formCount++;
        totalFormsInput.value = formCount;
    });
}