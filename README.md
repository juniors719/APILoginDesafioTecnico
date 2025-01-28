# API de Usuários - Desafio Técnico

## Descrição

Esta é uma API simples para o gerenciamento de usuários. Ela oferece endpoints para login, registro, listagem de usuários, edição e exclusão de usuários, entre outros.

**Versão da API**: 1.0  
**Desenvolvedor**: [Djalma Júnior](https://github.com/juniors719)

## Funcionalidades

- **Autenticação**: Login, logout, e refresh do token.
- **Gerenciamento de Usuários**: Criação, atualização, exclusão e listagem de usuários.
- **Segurança**: Proteção de rotas com JWT Bearer Token.

## Requisitos

- **Python 3.12+**
- **Docker** (para rodar com Docker Compose)
- **Docker Compose** (para orquestração)
  
## Instalação

### 1. Configuração do Ambiente Virtual (venv)

Caso não esteja usando Docker, você pode rodar a API localmente com um ambiente virtual em Python. Para isso:

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd <diretorio-do-repositorio>