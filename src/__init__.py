from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from .utils.database import init_db, db
from src.routes.auth_routes import auth_ns
from datetime import timedelta

jwt = JWTManager()
api = Api()
migrate = Migrate()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        init_db()

    api.init_app(app, version='1.0', title='API de Usuários - Desafio Técnico', description='Uma API simples para gerenciamento de usuários')
    api.add_namespace(auth_ns)


    @app.route('/hello')
    def index():
        return "hello world"

    return app
