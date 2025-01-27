from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from src.models import User, TokenBlocklist
from src.utils.database import db

auth_ns = Namespace('auth', description='Operações de autenticação')

user_model = auth_ns.model('User', {
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('register_user')
    @auth_ns.expect(user_model, validate=True)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Missing required fields')
    @auth_ns.response(409, 'Email already registered')
    def post(self):
        """
        Endpoint para registrar um novo usuário
        """
        data = request.get_json()
        user = User.get_by_email(email=data['email'])

        if not data.get('name') or not data.get('email') or not data.get('password'):
            return {"error": "Missing required fields"}, 400

        if user is not None:
            return {"error": "Email already registered"}, 409

        new_user = User(name=data['name'], email=data['email'])
        new_user.set_password(data['password'])
        new_user.save()
        return {"message": "User registered"}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successfully')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """
        Endpoint para login de usuários, que retorna tokens de acesso e de atualização.
        """
        data = request.get_json()
        user = User.get_by_email(email=data['email'])
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "message": "Login successful",
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }, 200

        return {"error": "Invalid credentials"}, 401

@auth_ns.route('/whoami')
class Whoami(Resource):
    @jwt_required()
    @auth_ns.response(200, 'User details retrieved successfully')
    @auth_ns.response(401, 'Unauthorized, invalid or expired token')
    @auth_ns.response(404, 'User not found')
    def get(self):
        """
        Endpoint protegido que retorna os detalhes do usuário autenticado.
        """
        user_id = get_jwt_identity()  # Recupera o ID do usuário a partir do token JWT
        user = User.query.get(user_id)  # Busca o usuário no banco de dados com o ID

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }, 200
