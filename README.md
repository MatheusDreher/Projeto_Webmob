# 🎮 GameMarket: Mercado de Jogos, Consoles e Acessórios

**Projeto da disciplina de Desenvolvimento Web Mobile**

Este projeto é um marketplace funcional full-stack desenvolvido com **Django (Python)** no backend e **Tailwind CSS** para o frontend. O foco principal é a **responsividade (Web Mobile)**, garantindo que o catálogo e todas as funcionalidades sejam perfeitas em dispositivos móveis.

---

## 🎯 Objetivo do Projeto

Criar uma plataforma onde um usuário/vendedor possa:

- Ver um catálogo de produtos totalmente responsivo (Web Mobile).
- Realizar Login e Cadastro.
- Anunciar (Criar, Editar, Excluir) seus próprios produtos.
- Comprar produtos de outros vendedores (funcionalidade de carrinho e checkout simulado).
- Visualizar e gerenciar seus próprios anúncios na área de Painel do Vendedor.

---

## 📱 Aplicação Mobile (Ionic + Angular)

O projeto foi estendido com uma aplicação móvel dedicada, desenvolvida com **Ionic Framework** e **Angular**, que consome o backend Django através de uma **API REST**.

### Arquitetura Mobile

- **Frontend:** Ionic Framework + Angular (para experiência nativa em iOS e Android).
- **Backend:** Django REST Framework (DRF) para expor os dados e a lógica de negócio.
- **Comunicação:** API RESTful com autenticação **JWT (JSON Web Tokens)**.

### Funcionalidades Mobile

O aplicativo móvel replica as principais funcionalidades do site, oferecendo uma experiência otimizada para dispositivos móveis:

- Catálogo de produtos com navegação otimizada.
- Login e Registro de usuários.
- Carrinho de compras e Checkout.
- Acesso a recursos nativos (como armazenamento local e notificações).

---

## ✅ Requisitos da Disciplina Atendidos

| Requisito | Implementação no GameMarket |
|-----------|----------------------------|
| **Frontend Web** | Layout usando HTML + Tailwind CSS (via CDN) para estética limpa e responsividade. |
| **Versão Mobile** | O site é totalmente responsivo (ajustável ao celular) e utiliza o princípio Mobile-First do Tailwind. O menu de navegação do desktop se adapta em links de ação e ícones no mobile. |
| **Backend** | Desenvolvido em Django, com separação de lógica em models, views e forms. |
| **Modelagem de Dados** | Modelagem completa de Produto, User (nativo do Django) e Pedido (para registrar transações). |
| **APIs** | (Sugestão para Futuro) Pronta para ser integrada com Django REST Framework. |
| **Segurança** | Áreas internas protegidas com `@login_required` e formulários com `{% csrf_token %}`. Controle de acesso rigoroso para Edição/Exclusão (somente o vendedor pode alterar seu produto). |
| **Usabilidade** | Formulário de Anúncio com lógica dinâmica (campos aparecem por categoria), ajuste de redimensionamento (`resize: none;`) e espaçamento correto de labels. |

---

## 🧱 Arquitetura e Estrutura do Projeto

O projeto segue a estrutura padrão de aplicações do Django, onde `gamemarket` é o projeto principal e `market` é a aplicação que contém toda a lógica de negócio.

```
gamemarket/
│
├─ gamemarket/            # Configurações principais (settings.py, urls.py)
├─ market/               # App Principal do Marketplace
│  ├─ migrations/
│  ├─ templatetags/      # Para filtros customizados (Ex: 'split')
│  ├─ templates/market/  # Todos os templates HTML (.html)
│  ├─ admin.py           # Configurações do painel admin
│  ├─ models.py          # Produtos, Pedidos, Vendedor (User)
│  ├─ forms.py           # Formulários para Anúncio e Checkout
│  ├─ serializers.py     # Serializadores para a API REST
│  └─ api_views.py       # ViewSets da API REST
│
├─ market-mobile/        # Projeto App Mobile (Ionic + Angular)
│  ├─ src/               # Código-fonte do App Mobile
│  └─ ...
│
└─ manage.py
```

---

## 🛠️ Detalhes de Implementação

### 1. Modelagem de Dados (market/models.py)

- **Produto**: Relacionado a User via ForeignKey (vendedor). Inclui campos de especificação condicional:
  - **Jogos**: `genero`, `classificacao_etaria`
  - **Consoles**: `cpu_gpu`, `memoria_ram`
  - **Acessórios**: `compatibilidade`

- **Pedido**: Registra a transação, incluindo comprador, vendedor_original e dados de entrega.

- **Upload**: Utiliza o `ImageField` para uploads de imagens, dependendo da biblioteca Pillow.

### 2. Lógica de Transação e Integridade

- O processo de checkout é encapsulado em uma transação atômica (`transaction.atomic`) para garantir que o estoque seja reduzido apenas se o pedido for salvo com sucesso.
- O estoque (`product.estoque`) é reduzido após o checkout.
- Produtos com estoque zerado são removidos da visualização do catálogo.

### 3. Frontend Responsivo

- **Navbar**: Layout adaptativo (desktop wide, mobile sanduíche) com Tailwind CSS, garantindo usabilidade em web mobile.
- **Catálogo**: Utiliza um layout de grid que muda de `grid-cols-1` (mobile) para `grid-cols-4` (desktop), preenchendo a tela de forma eficiente.
- **Formulários**: Largura controlada e espaçamento otimizado para fácil leitura em telas pequenas.

---

## 🚀 Requisitos de Sistema e Setup

### Requisitos de Software

- Python (3.10+)
- pip
- Django (5.x)
- Pillow
- django-widget-tweaks

### Setup Local

```bash
# 1. Instalação de dependências
pip install django Pillow django-widget-tweaks

# 2. Setup do Banco de Dados e Migrações
python manage.py makemigrations market
python manage.py migrate

# 3. Criação do Administrador
python manage.py createsuperuser

# 4. Execução do Servidor
python manage.py runserver
```

O site estará acessível em: **http://127.0.0.1:8000/**

---

## 📝 Informações do Projeto

- **Projeto**: GameMarket
- **Disciplina**: Desenvolvimento Web Mobile
- **Professor(a)**: Thiago Almeida
- **Desenvolvedor**: Matheus Henrique Dreher dos Santos
