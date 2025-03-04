# Base de Conhecimento

Sistema de gerenciamento de conhecimento desenvolvido com Python e Flask, permitindo o registro e consulta de tutoriais, soluções e documentações.

## 🛠 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- Bootstrap 5

## 📁 Estrutura do Projeto
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ └── templates/
│ ├── base.html
│ ├── index.html
│ ├── article.html
│ └── article_form.html
│
├── config.py
└── run.py

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

## 📋 Próximas Atualizações Planejadas

- [ ] Editor rich text para artigos
- [ ] Sistema de comentários
- [ ] Upload de imagens
- [ ] Exportação de artigos em PDF
- [ ] Sistema de versões dos artigos
- [ ] Sistema de favoritos
- [ ] Preview de markdown
- [ ] Estatísticas de visualização
- [ ] Sistema de busca com filtros avançados

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Changelog

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
