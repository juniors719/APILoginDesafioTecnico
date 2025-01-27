from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
api = Api()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = getenv('JWT_ACCESS_TOKEN_EXPIRES')

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    @app.route('/hello')
    def index():
        return "hello world"

    return app
