# Base de Conhecimento

Sistema de gerenciamento de conhecimento desenvolvido com Python e Flask, permitindo o registro e consulta de tutoriais, soluções e documentações.

## 🛠 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- Bootstrap 5
- Bootstrap Icons
- Editor Rich Text personalizado

## 📁 Estrutura do Projeto
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ ├── auth/
│ │ └── routes.py
│ ├── static/
│ │ └── css/
│ │     └── style.css
│ └── templates/
│   ├── admin/
│   │ ├── categories.html
│   │ ├── roles.html
│   │ ├── tags.html
│   │ └── users.html
│   ├── auth/
│   │ ├── login.html
│   │ └── register.html
│   ├── base.html
│   ├── index.html
│   ├── article.html
│   └── article_form.html

## 🚀 Funcionalidades Atuais

- [x] Criação de artigos
- [x] Listagem de artigos com cards interativos
- [x] Visualização detalhada de artigos
- [x] Edição de artigos
- [x] Exclusão de artigos com confirmação
- [x] Busca por título e conteúdo
- [x] Categorização de conteúdo
- [x] Sistema de tags
- [x] Interface responsiva
- [x] Sistema de autenticação de usuários
- [x] Proteção de rotas por login
- [x] Associação de artigos com autores
- [x] Menu dropdown unificado
- [x] Gerenciamento de usuários
- [x] Gerenciamento de categorias
- [x] Gerenciamento de tags
- [x] Interface melhorada com animações
- [x] Cards com efeitos hover
- [x] Sistema de busca aprimorado
- [x] Layout responsivo otimizado
- [x] Feedback visual para ações
- [x] Sistema de roles (admin/usuário)
- [x] Editor rich text personalizado
- [x] Sistema de permissões
- [x] Breadcrumbs para navegação
- [x] Modais de confirmação
- [x] Multi-seleção de tags
- [x] Comandos CLI para gerenciamento
- [x] Proteção CSRF
- [x] Filtros Jinja personalizados

## 📋 Próximas Atualizações Planejadas

- [ ] Sistema de comentários
- [ ] Upload de imagens
- [ ] Exportação de artigos em PDF
- [ ] Sistema de versões dos artigos
- [ ] Sistema de favoritos
- [ ] Preview de markdown
- [ ] Estatísticas de visualização
- [ ] Sistema de busca com filtros avançados
- [ ] Editor com suporte a imagens
- [ ] Sistema de notificações
- [ ] Histórico de edições
- [ ] Tags coloridas personalizáveis

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Changelog

### v0.6.0 (05/03/2025)
- Implementado editor rich text personalizado
- Adicionado sistema de permissões
- Melhorado sistema de roles
- Adicionado comandos CLI para gerenciamento
- Implementado proteção CSRF
- Adicionado filtros Jinja personalizados
- Melhorada estrutura de arquivos do projeto
- Implementado breadcrumbs para navegação
- Adicionado suporte a multi-seleção de tags

### v0.5.0 (05/03/2025)
- Removido TinyMCE em favor do editor personalizado
- Melhorada visualização de artigos com suporte a HTML
- Adicionada barra de ferramentas de formatação
- Suporte a diferentes estilos de texto e listas

### v0.4.0 (04/03/2025)
- Removido debug information dos templates
- Atualizado layout do navbar com dropdown unificado
- Melhorado design da interface com novas cores e tipografia
- Adicionado animações e feedback visual
- Implementado sistema de busca aprimorado
- Otimizado visual dos cards e elementos da interface
- Adicionado gerenciamento de tags e categorias
- Implementado sistema de roles

### v0.3.0 (04/03/2025)
- Implementado sistema de autenticação de usuários
- Adicionado relacionamento entre usuários e artigos
- Proteção de rotas por login
- Adicionado menu de usuário na navegação

### v0.2.0 (04/03/2025)
- Interface completamente redesenhada
- Adicionado sistema de cards com animações
- Implementado layout responsivo

### v0.1.2 (04/03/2025)
- Adicionada funcionalidade de edição de artigos
- Adicionada funcionalidade de exclusão de artigos
- Implementado modal de confirmação para exclusão
- Interface completamente redesenhada
- Adicionado sistema de cards com animações
- Implementado layout responsivo
- Melhorado sistema de navegação
- Adicionados ícones em toda interface
- Melhorada organização do conteúdo
- Adicionada barra de busca centralizada
- Implementado feedback visual para ações

### v0.1.1 (28/02/2025)
- Adicionada visualização detalhada de artigos
- Interface melhorada para exibição de artigos individuais

### v0.1.0 (28/02/2025)
- Implementação inicial do projeto
- CRUD básico de artigos
- Sistema de busca simples
- Interface básica com Bootstrap

## 🚀 Deploy

### Deploy no Render

1. Crie uma conta no [Render](https://render.com)
2. Conecte seu repositório GitHub
3. Clique em "New Web Service"
4. Selecione seu repositório
5. Configure:
   - Name: base-conhecimento (ou outro nome)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
6. Clique em "Create Web Service"

### Variáveis de Ambiente
Configure as seguintes variáveis no Render:
- `FLASK_APP=run.py`
- `FLASK_ENV=production`
- `SECRET_KEY` (será gerado automaticamente)
- `DATABASE_URL` (será fornecido pelo Render se usar PostgreSQL)
