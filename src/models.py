from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .utils.database import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name} {self.email}>"

    def set_password(self, password):
        """
        Define uma senha hash
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checa se a senha passada bate com a senha guardada
        """
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_email(cls, email):
        """
        Get de um usuário pelo email
        """
        return cls.query.filter_by(email=email).first()

    def save(self):
        """
        Salva o usuário no banco de dados
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()  # Reverts the transaction
            raise Exception(f"Erro ao salvar usuário: {e}")

    def delete(self):
        """
        Deleta o usuário do banco de dados
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()  # Reverts the transaction
            raise Exception(f"Erro ao excluir usuário: {e}")


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
