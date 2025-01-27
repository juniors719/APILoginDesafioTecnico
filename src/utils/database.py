from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
from flask import current_app

db = SQLAlchemy()


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
        else:
            current_app.logger.info("Tabelas já existem. Nenhuma ação necessária.")

        connection.close()
