# API de Usuários - Desafio Técnico

## Descrição

Esta é uma API simples para o gerenciamento de usuários. Ela oferece endpoints para login, registro, listagem de
usuários, edição e exclusão de usuários, entre outros.

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
   ```
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
3. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```
   no Windows:
   ```bash
   .\venv\Scripts\activate
   ```
4. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```
5. Rode a aplicação
   ```bash
   docker-compose up --build
   ```
6. A API estará disponível em `http://localhost:5000`

## Endpoints

Abaixo está uma breve descrição dos principais endpoints da API.

### Autenticação

- `POST /auth/login`
  Realiza login de um usuário e retorna tokens de acesso e de atualização.
- `POST /auth/logout`
  Revoga o token de acesso do usuário.
- `GET /auth/refresh`
  Gera um novo token de acesso usando o refresh token.
- `POST /auth/register`
  Registra um novo usuário.
- `GET /auth/whoami`
  Retorna os detalhes do usuário autenticado.

### Usuários

- `GET /users`
  Lista todos os usuários com paginação.
- `GET /users/{user_id}`
  Retorna os detalhes de um usuário específico.
- `PUT /users/{user_id}`
  Atualiza informações de um usuário, como torná-lo administrador.
- `DELETE /users/{user_id}`
  Deleta um usuário pelo ID.

## Testes

Esta API inclui uma suíte de testes automatizados para garantir a confiabilidade das funcionalidades implementadas. Para rodar os testes, siga os passos abaixo:

1. Certifique-se de que a variável de ambiente FLASK_ENV esteja configurada para o modo de teste:
```bash
FLASK_ENV=testing
```
Adicione essa configuração ao arquivo .env, se necessário.

2. Execute os testes com o seguinte comando:
```bash
pytest --cov=app tests/ -v
```

## Documentação Swagger

A documentação interativa da API está disponível através do Swagger em: `http://localhost:5000/swagger`
Aqui, você pode explorar todos os endpoints da API, enviar requisições e visualizar as respostas.

## Segurança

Esta API usa autenticação via JWT (JSON Web Token). Todos os endpoints que exigem autenticação necessitam de um token
válido no cabeçalho Authorization no formato Bearer <token>.


