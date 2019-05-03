from flask import request
from flask_restplus import Resource, marshal

from app.api.namespaces.user_namespaces import public_user, user, new_user
from app.api.namespaces.users_namespace import users_ns
from app.api.security.authentication import token_auth
from app.models import User
from app.services.user_service import get_all_users, email_exists, username_exists, save_user
from app.utils import collection_as_dict


@users_ns.route('', strict_slashes=False, endpoint='users_ep')
@users_ns.response(500, 'Internal Server Error')
class UsersResource(Resource):

    @users_ns.response(200, 'List all users', [public_user])
    @users_ns.response(401, 'Unauthorized')
    @token_auth.login_required
    def get(self):
        """List all users"""
        return marshal(collection_as_dict(get_all_users()), public_user), 200

    @users_ns.expect(new_user, validate=True)
    @users_ns.response(201, 'User successfully created', user, headers={'location': 'The user\'s location'})
    @users_ns.response(400, 'Bad request')
    @users_ns.response(409, 'User already exists')
    @users_ns.doc(security=None)
    def post(self):
        """Create a new user"""
        json_data = request.get_json(force=True)
        if email_exists(json_data['email']):
            users_ns.abort(409, "Email already registered")
        if username_exists(json_data['username']):
            users_ns.abort(409, "Username already exists")
        future_user = User()
        future_user.username = json_data['username']
        future_user.name = json_data['name']
        future_user.surname = json_data['surname']
        future_user.email = json_data['email']
        future_user.set_password(json_data['password'])
        save_user(future_user)
        return marshal(future_user.as_dict(), user), 201, {'Location': '{}/{}'.format(request.url, future_user.id)}
