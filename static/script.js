// Espera o documento carregar completamente
// O 'DOMContentLoaded' é um evento disparado pelo navegador quando toda a estrutura 
// HTML da página foi completamente carregada e analisada pelo navegador (o DOM está pronto).
// Isso garante que, quando o código dentro desta função for executado, todos os 
// elementos HTML (como o formulário e o input de CPF) já existem e podem ser encontrados.
document.addEventListener("DOMContentLoaded", function() {
            
    // Usa o método 'getElementById' para encontrar o elemento HTML que tem o atributo id="cpf".
    // A constante 'cpfInput' agora armazena uma referência a esse campo de input.
    const cpfInput = document.getElementById("cpf");
    // Faz o mesmo para o formulário, encontrando o elemento com id="colaborador-form".
    const form = document.getElementById("colaborador-form"); // Pega o formulário


    // Antes de tentar adicionar 'event listeners' (escutadores de eventos),
    // é crucial verificar se os elementos foram realmente encontrados na página atual.
    // Se este script for carregado em uma página que NÃO tem o formulário ou o campo CPF 
    // (como a página 'index.html'), 'form' ou 'cpfInput' seriam 'null'.
    // Tentar adicionar um listener a 'null' causaria um erro e quebraria o script.
    // Este 'if' garante que o código da máscara só execute se AMBOS os elementos existirem.
    if (form && cpfInput) {

        // Máscara de CPF - Event Listener no Input
        // Adiciona um "escutador" ao campo 'cpfInput' que será acionado toda vez que o 
        // evento 'input' ocorrer. O evento 'input' é disparado sempre que o valor do campo muda 
        // (seja digitando, colando, deletando).
        cpfInput.addEventListener("input", function(e) {
            // 'e' é o objeto do evento, que contém informações sobre o que aconteceu.
            // 'e.target' é o próprio elemento <input> onde o evento ocorreu.
            // 'e.target.value' é o valor ATUAL do campo de input.

            // 1. Limpeza do Valor: Remove caracteres não numéricos
            // ----------------------------------------------------
            // Pega o valor atual do input (e.target.value).
            // Usa o método 'replace' com uma expressão regular (RegExp):
            //   - /\D/g : 
            //     - \D : Corresponde a qualquer caractere que NÃO seja um dígito (0-9).
            //     - g  : Flag "global", significa que a substituição deve ocorrer em TODAS 
            //            as ocorrências na string, não apenas na primeira.
            //   - "" : O segundo argumento do 'replace' é a string de substituição. 
            //          Uma string vazia significa "remova o caractere encontrado".
            // O resultado é que 'value' conterá APENAS os dígitos digitados pelo usuário.
            let value = e.target.value.replace(/\D/g, ""); 

            // 2. Limitação de Comprimento: Máximo de 11 dígitos
            // -------------------------------------------------
            // Verifica se a string 'value' (apenas com dígitos) tem mais de 11 caracteres.
            if (value.length > 11) {
                // Se tiver, usa 'substring(0, 11)' para pegar apenas os primeiros 11 caracteres,
                // efetivamente impedindo que o usuário digite mais do que os 11 dígitos de um CPF.
                value = value.substring(0, 11);
            }

            // 3. Aplicação da Máscara (Formatação com Pontos e Traço)
            // --------------------------------------------------------
            // Esta série de 'if / else if' aplica a formatação visual do CPF (XXX.XXX.XXX-XX)
            // progressivamente, à medida que o usuário digita.

            // Se o usuário digitou 10 ou 11 dígitos...
            if (value.length > 9) {
                // Aplica a formatação completa XXX.XXX.XXX-XX.
                // Usa 'replace' com uma RegExp que captura grupos de dígitos:
                //   - (\d{3}) : Captura exatamente 3 dígitos (grupo 1 - $1)
                //   - (\d{3}) : Captura os próximos 3 dígitos (grupo 2 - $2)
                //   - (\d{3}) : Captura os próximos 3 dígitos (grupo 3 - $3)
                //   - (\d{2}) : Captura os últimos 2 dígitos (grupo 4 - $4)
                // A string "$1.$2.$3-$4" reconstrói a string usando os grupos capturados,
                // inserindo os pontos e o traço nos lugares corretos.
                value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
            
            // Senão, se o usuário digitou entre 7 e 9 dígitos...
            } else if (value.length > 6) {
                // Aplica a formatação parcial XXX.XXX.XXX.
                //   - (\d{3}) : Grupo 1 ($1)
                //   - (\d{3}) : Grupo 2 ($2)
                //   - (\d{1,3}) : Captura de 1 a 3 dígitos restantes (grupo 3 - $3)
                // Formata como "$1.$2.$3".
                value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, "$1.$2.$3");

            // Senão, se o usuário digitou entre 4 e 6 dígitos...
            } else if (value.length > 3) {
                // Aplica a formatação inicial XXX.XXX.
                //   - (\d{3}) : Grupo 1 ($1)
                //   - (\d{1,3}) : Captura de 1 a 3 dígitos restantes (grupo 2 - $2)
                // Formata como "$1.$2".
                value = value.replace(/(\d{3})(\d{1,3})/, "$1.$2");
            }
            // Se tiver 3 ou menos dígitos, nenhuma formatação é aplicada ainda.

            // 4. Atualização do Valor no Campo Input
            // ---------------------------------------
            // Define o valor VISÍVEL do campo input (<input id="cpf">) como a string 
            // 'value', que agora está limpa (só dígitos) e formatada com a máscara.
            // Isso faz com que o usuário veja o CPF sendo formatado em tempo real.
            e.target.value = value;
        }); 
        
    } 
}); 

// Espera o documento carregar
document.addEventListener("DOMContentLoaded", function() {
    
    // Pega os elementos do DOM
    const menuTrigger = document.getElementById("user-menu-trigger");
    const userMenu = document.getElementById("user-menu");

    // Garante que os elementos existem antes de adicionar o script
    if (menuTrigger && userMenu) {
        
        // 1. Abre/Fecha o menu ao clicar no rodapé (gatilho)
        menuTrigger.addEventListener("click", function(event) {
            // Impede que o clique "vaze" para o 'window' e feche o menu
            event.stopPropagation(); 
            // Adiciona ou remove a classe .show
            userMenu.classList.toggle("show");
        });

        // 2. Fecha o menu se o usuário clicar em qualquer outro lugar da tela
        window.addEventListener("click", function(event) {
            // Se o menu estiver aberto (.show) E o clique NÃO foi dentro dele
            if (userMenu.classList.contains("show") && !userMenu.contains(event.target)) {
                userMenu.classList.remove("show");
            }
        });
    }
});