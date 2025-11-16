# PROJETIC_EPI: Sistema de Gerenciamento de EPIs 👷🚧

## 🚀 Visão Geral

Este projeto é um Sistema Web completo para o Gerenciamento de Equipamentos de Proteção Individual (EPIs), desenvolvido como parte do curso Técnico em Desenvolvimento de Sistemas. O objetivo é atender à necessidade de uma construtora que busca modernizar seu controle de estoque, rastrear empréstimos e garantir a segurança e conformidade no ambiente de trabalho.

O sistema é dividido em uma **página pública** (landing page) e um **painel de administração** privado e seguro, acessível apenas por login.

---

## ✨ Funcionalidades Principais

O sistema é modularizado em quatro aplicativos principais:

### 🔐 Módulo de Autenticação (App: `core`)
* **Landing Page:** Uma "Home Page" pública, moderna e visualmente atraente que descreve o propósito do projeto.
* **Sistema de Login:** Uma página de login segura (`/login/`) para administradores do sistema.
* **Proteção de Rotas:** O painel de gerenciamento (`/sistema/`) é 100% protegido. Usuários não logados são automaticamente redirecionados para a tela de login.
* **Sistema de Logout:** Funcionalidade de "Sair" segura que redireciona o usuário de volta para a Home Page.

### 👥 Módulo de Colaboradores (App: `colaboradores`)
* **CRUD Completo:** Cadastro, Leitura, Edição e Exclusão de colaboradores.
* **Validação de Matrícula:** Impede o cadastro de matrículas duplicadas.
* **Busca e Filtro:** Permite pesquisar colaboradores por nome, matrícula ou função.
* **Interface com Modais:** Utiliza modais de confirmação para exclusão e feedback de sucesso/erro, evitando a troca desnecessária de telas.

### 📦 Módulo de Estoque (App: `equipamentos`)
* **CRUD Completo:** Cadastro, Leitura, Edição e Exclusão de equipamentos (EPIs).
* **Controle de Estoque:** Gerenciamento separado de `estoque_total` e `estoque_disponivel`.
* **Validação de Negócio:**
    * Impede o cadastro de equipamentos com o mesmo nome (`unique=True`).
    * Impede o cadastro de equipamentos com estoque total igual a zero.
* **Segurança:** Impede a exclusão de um equipamento se houver itens dele atualmente emprestados.

### 🚚 Módulo de Empréstimos (App: `emprestimos`)
* **Dashboard de KPIs:** Tela principal com indicadores visuais (KPIs) de empréstimos **Ativos**, **Atrasados** e **Devolvidos**.
* **Sistema de "Carrinho" (FormSet):** Permite o registro de um novo empréstimo para um colaborador com **múltiplos itens e quantidades** de uma só vez.
* **Controle de Estoque Ativo:**
    * O formulário de "Novo Empréstimo" só exibe EPIs com `estoque_disponivel > 0`.
    * Impede o empréstimo de uma quantidade maior do que a disponível.
    * **Subtrai** do `estoque_disponivel` automaticamente quando um empréstimo é realizado.
* **Sistema de Devolução Parcial:**
    * Permite devolver partes de um item (ex: devolver 5 de 10 luvas).
    * O sistema calcula automaticamente a "Quantidade Pendente".
* **Histórico de Devoluções:**
    * Cria um **log de histórico** para cada devolução parcial, registrando a quantidade, a data e o status (Devolvido, Danificado, Perdido).
    * **Adiciona** ao `estoque_disponivel` automaticamente quando um item é "Devolvido" ou "Danificado".
* **Atualização Automática de Status:**
    * Itens de empréstimo mudam de `PENDENTE` para `CONCLUÍDO` quando a quantidade pendente chega a zero.
    * Empréstimos mudam de `ATIVO` para `DEVOLVIDO` quando todos os seus itens são concluídos.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Django 5.2
* **Frontend:** HTML5, CSS3 (CSS Grid, Flexbox), JavaScript (ES6+)
* **Banco de Dados:** SQLite 3 (para desenvolvimento)
* **Controle de Versão:** Git, GitHub
* **Bibliotecas JS:** Feather Icons (para ícones), AOS (para animações de scroll)

---

## 🚀 Configuração e Execução do Projeto

Siga os passos abaixo para configurar e rodar o projeto localmente:

1.  **Pré-requisitos:**
    * Python 3.8 ou superior instalado.
    * Git instalado.

2.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/pedroviniciospereira/PROJETIC_EPI.git](https://github.com/pedroviniciospereira/PROJETIC_EPI.git)
    cd PROJETIC_EPI
    ```

3.  **Crie e Ative um Ambiente Virtual:**
    * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * No macOS/Linux:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

4.  **Instale as Dependências:**
    *(Opcional: Se existir um arquivo `requirements.txt`, use `pip install -r requirements.txt`)*
    ```bash
    pip install django
    ```

5.  **Aplique as Migrações do Banco de Dados:**
    Este comando cria todas as tabelas (Colaborador, Equipamento, Empréstimo, etc.) no `db.sqlite3`.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crie um Superusuário (Admin):**
    Este é o usuário que você usará para acessar o painel `/sistema/`.
    ```bash
    python manage.py createsuperuser
    ```
    *(Siga as instruções para definir nome de usuário e senha).*

7.  **Execute o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

8.  **Acesse o Sistema:**
    * Abra `http://127.0.0.1:8000/` para ver a **Home Page** pública.
    * Acesse `http://127.0.0.1:8000/login/` para fazer o **Login**.
    * Após o login, você será redirecionado para `http://127.0.0.1:8000/sistema/` (o painel de gerenciamento).
