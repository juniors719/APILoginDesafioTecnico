from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from .utils.database import init_db, db

jwt = JWTManager()
api = Api()
migrate = Migrate()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = getenv('JWT_ACCESS_TOKEN_EXPIRES')

    jwt.init_app(app)
    api.init_app(app)
    db.init_app(app)
    with app.app_context():
        init_db()

    @app.route('/hello')
    def index():
        return "hello world"

    return app
