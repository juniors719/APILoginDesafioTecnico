from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

from src.models import User

users_ns = Namespace('users', description='Gerenciamento de usuários')

user_model = users_ns.model('User', {
    'id': fields.String(readOnly=True, description='ID do usuário'),
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'is_admin': fields.Boolean(description='Define se o usuário é administrador')
})

update_user_model = users_ns.model('UpdateUser', {
    'name': fields.String(description='Novo nome do usuário'),
    'is_admin': fields.Boolean(description='Tornar o usuário administrador (True/False)')
})

user_list_output_model = users_ns.model('UserListOutput', {
    'users': fields.List(fields.Nested(user_model), description='Lista de usuários'),
    'total': fields.Integer(description='Total de usuários', required=True),
    'pages': fields.Integer(description='Total de páginas', required=True),
    'current_page': fields.Integer(description='Página atual', required=True),
    'per_page': fields.Integer(description='Itens por página', required=True),
})


@users_ns.route('/')
class UserList(Resource):
    @users_ns.doc('list_users', security='Bearer Auth')
    @jwt_required()
    @users_ns.param('page', 'Número da página para a consulta de usuários', type=int, default=1)
    @users_ns.param('per_page', 'Número de itens por página', type=int, default=10)
    @users_ns.response(200, 'Usuários listados com sucesso', model=[user_model])
    @users_ns.marshal_list_with(user_list_output_model)
    def get(self):
        """
        Lista todos os usuários com paginação.
        """
        page = request.args.get('page', 1, type=int)  # Página atual (default: 1)
        per_page = request.args.get('per_page', 10, type=int)  # Itens por página (default: 10)

        if page < 1:
            return {"error": "O parâmetro 'page' deve ser maior ou igual a 1."}, 400
        if per_page < 1:
            return {"error": "O parâmetro 'per_page' deve ser maior ou igual a 1."}, 400

        users = User.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page,
            'per_page': users.per_page
        }, 200


@users_ns.route('/<uuid:user_id>')
class UserDetail(Resource):
    @users_ns.doc('get_user', security='Bearer Auth')
    @jwt_required()
    @users_ns.response(200, 'Usuário encontrado', model=user_model)
    @users_ns.response(404, 'Usuário não encontrado')
    @users_ns.marshal_with(user_model)
    def get(self, user_id):
        """
        Retorna detalhes de um usuário específico.
        """
        user = User.query.get(str(user_id))
        if not user:
            return {"error": "Usuário não encontrado"}, 404
        return user.to_dict(), 200

    @users_ns.doc('update_user', security='Bearer Auth')
    @users_ns.expect(update_user_model, validate=True)
    @jwt_required()
    @users_ns.response(200, 'Usuário atualizado com sucesso', model=user_model)
    @users_ns.response(404, 'Usuário não encontrado')
    @users_ns.marshal_with(user_model)
    def put(self, user_id):
        """
        Atualiza as informações de um usuário, como torná-lo administrador.
        """
        user = User.query.get(str(user_id))
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        data = users_ns.payload
        if 'name' in data:
            user.name = data['name']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        user.save()
        return user.to_dict(), 200

    @users_ns.doc('delete_user', security='Bearer Auth')
    @jwt_required()
    @users_ns.response(204, 'Usuário deletado com sucesso')
    @users_ns.response(404, 'Usuário não encontrado')
    def delete(self, user_id):
        """
        Deleta um usuário pelo ID.
        """
        user = User.query.get(str(user_id))
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        user.delete()
        return {"message": "Usuário deletado com sucesso"}, 204
