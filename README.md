# PROJETIC_EPI: Sistema de Gestão Inteligente de Segurança 👷🚧

## 🚀 Visão Geral

O **PROJETIC EPI** é um sistema web completo desenvolvido para modernizar a gestão de Equipamentos de Proteção Individual (EPIs) em construtoras e empresas. O foco é garantir a conformidade com a segurança do trabalho (NR-6), controlar o estoque em tempo real e rastrear empréstimos de forma detalhada.

O sistema possui uma **Landing Page pública** moderna para apresentação e um **Painel Administrativo** seguro para a gestão diária.

---

## ✨ Funcionalidades Principais

### 🖥️ Interface & Experiência
* **Landing Page Moderna:** Página inicial com design profissional, estatísticas e apresentação de recursos.
* **Dashboard Interativo:** Visão geral com KPIs de empréstimos (Ativos, Atrasados, Devoluções).
* **Design Responsivo:** Funciona bem em computadores e dispositivos móveis.

### 🔐 Segurança & Perfil (App: `core`)
* **Acesso Restrito:** Sistema protegido por login.
* **Gestão de Perfil:** O usuário pode alterar seus dados, senha e fazer **upload de foto de perfil**.
* **Segurança Reforçada:** Configurações ajustadas para ambientes de desenvolvimento em nuvem (Codespaces) e proteção contra ataques CSRF.

### 👥 Gestão de Colaboradores (App: `colaboradores`)
* **Cadastro Completo:** Registro de nome, matrícula (única), função e status.
* **Validações:** Impede duplicidade de matrículas.
* **Busca Inteligente:** Filtre colaboradores por nome ou matrícula rapidamente.

### 📦 Controle de Estoque (App: `equipamentos`)
* **Inventário de EPIs:** Cadastro de equipamentos com categoria, C.A. (Certificado de Aprovação) e quantidades.
* **Estoque Inteligente:** O sistema calcula automaticamente o `estoque_disponivel` com base nos empréstimos ativos.
* **Proteção de Dados:** Impede a exclusão de itens que ainda estão emprestados.

### 🚚 Gestão de Empréstimos (App: `emprestimos`)
* **Carrinho de Empréstimo:** Adicione múltiplos EPIs para um único colaborador em uma só transação.
* **Validação de Estoque:** O sistema impede empréstimos se não houver saldo disponível.
* **Devolução Parcial e Total:**
    * Permite devolver apenas parte dos itens (ex: devolver 1 luva de 2 emprestadas).
    * Registra o estado do item na devolução: **Devolvido**, **Danificado** ou **Perdido**.
* **Histórico Detalhado:** Rastreabilidade completa de cada item emprestado.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.12+, Django 5.2
* **Frontend:** HTML5, CSS3 (Glassmorphism, Flexbox, Grid), JavaScript Puro.
* **Banco de Dados:** SQLite 3 (Padrão)
* **Bibliotecas:**
    * `Pillow`: Processamento de imagens de perfil.
    * `Boxicons` & `Feather Icons`: Ícones vetoriais.

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
    pip install pillow
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
