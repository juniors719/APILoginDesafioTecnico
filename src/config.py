from src.models import User, TokenBlocklist
from datetime import timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'default-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Banco de dados em memória


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    DEBUG = False
    TESTING = False

def get_config(env):
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    elif env == 'production':
        return ProductionConfig
    raise ValueError(f"Invalid environment: {env}")


def configure_jwt(jwt, db):
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        user = User.query.get(identity)
        return {"is_admin": user.is_admin} if user else {"is_admin": False}

    @jwt.user_lookup_loader
    def user_lookup_callback(__jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Signature verification failed",
            "error": "invalid_token"
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request doesn't contain a valid token",
            "error": "authorization_header"
        }, 401

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        return token is not None
