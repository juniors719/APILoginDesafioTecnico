from datetime import timedelta
from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

from src.routes.auth_routes import auth_ns
from src.routes.user_routes import users_ns
from .config import configure_jwt
from .utils.database import init_db, db

jwt = JWTManager()
authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Adicione um acesso JWT neste modelo:    Bearer &lt;JWT&gt;"
    }
}

api = Api(
    version='1.0',
    title='API de Usuários - Desafio Técnico',
    description='Uma API simples para gerenciamento de usuários<br>Feito por Djalma Júnior - https://github.com/juniors719',
    authorizations=authorizations,
    security="Bearer Auth",
    contact="https://github.com/juniors719",
)
migrate = Migrate()


def create_app():
    load_dotenv()

    app = Flask("apilogin.app")

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    jwt.init_app(app)
    configure_jwt(jwt, db)
    db.init_app(app)
    with app.app_context():
        init_db()

    api.init_app(app)

    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)

    @app.route('/hello')
    def index():
        return "hello world"

    return app
