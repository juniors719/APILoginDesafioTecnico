from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Lista de usurios que serão inseridos no bd para fins de teste
users_data = [
    {'name': 'Administrador', 'email': 'admin@example.com', 'is_admin': True, 'password': 'admin123'},
    {'name': 'João Silva', 'email': 'joao.silva@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Maria Oliveira', 'email': 'maria.oliveira@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Ana Souza', 'email': 'ana.souza@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Carlos Mendes', 'email': 'carlos.mendes@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Beatriz Lima', 'email': 'beatriz.lima@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Lucas Almeida', 'email': 'lucas.almeida@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Mariana Costa', 'email': 'mariana.costa@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Pedro Henrique', 'email': 'pedro.henrique@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Fernanda Santos', 'email': 'fernanda.santos@example.com', 'is_admin': False, 'password': '12345678'}
]


def init_db():
    """
    Inicializa o banco de dados e cria as tabelas a partir do arquivo SQL.
    """
    with current_app.app_context():
        # Obtém a conexão
        connection = db.engine.connect()
        inspector = inspect(connection)

        if not inspector.has_table('users'):
            current_app.logger.info("Criando tabelas a partir do arquivo SQL...")
            with current_app.open_resource('utils/CreateDatabase.sql') as f:
                sql_commands = f.read().decode('utf8')
                for command in sql_commands.split(';'):
                    if command.strip():
                        db.session.execute(text(command))
                db.session.commit()
                current_app.logger.info("Tabelas criadas com sucesso!")
                insert_users()
        else:
            current_app.logger.info("Tabelas já existem. Nenhuma ação necessária.")

        connection.close()


def insert_users():
    """
    Função para inserir usuários no banco de dados.
    """
    from src.models import User
    for user in users_data:
        # Hash da senha antes de inserir
        hashed_password = generate_password_hash(user['password'])

        # Cria um objeto do usuário (assumindo que você tem uma classe User)
        new_user = User(
            name=user['name'],
            email=user['email'],
            password=hashed_password,
            is_admin=user['is_admin']
        )

        # Adiciona o usuário à sessão e commita
        db.session.add(new_user)
        db.session.commit()