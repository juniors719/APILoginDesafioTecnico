import pytest
from app import create_app
from src.utils.database import db
from werkzeug.security import generate_password_hash
from src.models import User

users_data = [
    {'name': 'Administrador', 'email': 'admin@example.com', 'is_admin': True, 'password': 'admin123'},
    {'name': 'João Silva', 'email': 'joao.silva@example.com', 'is_admin': False, 'password': '12345678'},
    {'name': 'Maria Oliveira', 'email': 'maria.oliveira@example.com', 'is_admin': False, 'password': '12345678'},
]

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def init_database_with_admin(app):
    with app.app_context():
        for user in users_data:
            new_user = User(
                name=user['name'],
                email=user['email'],
                is_admin=user['is_admin']
            )
            new_user.set_password(user['password'])
            db.session.add(new_user)
        db.session.commit()