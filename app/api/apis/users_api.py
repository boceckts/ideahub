from flask import request, g
from flask_restplus import Resource, marshal

from app.api.namespaces.user_namespaces import public_user, user, new_user
from app.api.namespaces.users_namespace import users_ns
from app.api.security.authentication import token_auth
from app.api.security.authorization import is_admin
from app.services.user_service import get_all_users, email_exists, username_exists, save_user_by_json, delete_all_users, \
    get_user_by_id, delete_user_by_id
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
        future_user = save_user_by_json(json_data)
        return marshal(future_user.as_dict(), user), 201, {'Location': '{}/{}'.format(request.url, future_user.id)}

    @users_ns.response(403, 'Forbidden')
    @token_auth.login_required
    def delete(self):
        """Delete all users (ADMIN)"""
        if not is_admin():
            users_ns.abort(403, 'You don\'t have sufficient rights to access this resource')
        delete_all_users()
        return '', 204


@users_ns.route('/<int:user_id>', strict_slashes=False)
@users_ns.response(401, 'Unauthorized')
@users_ns.response(403, 'Forbidden')
@users_ns.response(404, 'User not found')
@users_ns.response(500, 'Internal Server Error')
class UserResource(Resource):

    @users_ns.response(204, 'User was successfully deleted')
    @token_auth.login_required
    def delete(self, user_id):
        """Delete the user with the selected user_id (ADMIN)"""
        if not is_admin():
            users_ns.abort(403, 'You don\'t have sufficient rights to access this resource')
        if g.current_user.id == user_id:
            users_ns.abort(403, 'Admin user can not be deleted')
        if get_user_by_id(user_id) is None:
            users_ns.abort(404, 'User not found')
        delete_user_by_id(user_id)
        return '', 204
