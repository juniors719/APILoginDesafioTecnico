from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user, \
    get_jwt
from flask_restx import Namespace, Resource, fields

from src.models import User, TokenBlocklist

auth_ns = Namespace('auth', description='Operações de autenticação')

signup_model = auth_ns.model('SignUpModel', {
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

access_token_model = auth_ns.model('AccessToken', {
    'access_token': fields.String(required=True, description='Token de acesso JWT')
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('register_user')
    @auth_ns.expect(signup_model, validate=True)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Missing required fields')
    @auth_ns.response(409, 'Email already registered')
    def post(self):
        """
        Registrar um novo usuário
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
    @auth_ns.doc('login_user')
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successfully')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """
        Login de usuários, que retorna tokens de acesso e de atualização.
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
    @auth_ns.doc('whoami', security='Bearer Auth')
    @auth_ns.response(200, 'User details retrieved successfully')
    @auth_ns.response(401, 'Unauthorized, invalid or expired token')
    @auth_ns.response(404, 'User not found')
    def get(self):
        """
        Endpoint protegido que retorna os detalhes do usuário autenticado.
        """
        return {
            "name": current_user.name,
            "email": current_user.email
        }


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required()
    @auth_ns.doc(security='BearerAuth')
    @auth_ns.response(200, 'Refresh token retrieved successfully')
    @auth_ns.response(401, 'Unauthorized, invalid or expired token')
    def get(self):
        """
        Endpoint protegido que gera um novo token de acesso utilizando o refresh token
        """
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return {"access_token": new_access_token}, 200


@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    @auth_ns.doc('logout_user', security='Bearer Auth')
    @auth_ns.response(200, 'Logout successfully logged out')
    def get(self):
        """
        Revogar o token de acesso
        """
        jwt = get_jwt()
        jti = jwt['jti']
        token_type = jwt['type']
        token_blocklist = TokenBlocklist(jti=jti)
        token_blocklist.save()
        return {"message": f"{token_type} token revoked successfully"}, 200
