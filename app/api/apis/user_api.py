from flask import request
from flask_restplus import Resource, marshal

from app.api.namespaces.user_namespaces import user_ns, user, modify_user
from app.api.security.authentication import token_auth
from app.models import User
from app.services.user_service import get_current_user, edit_current_user, email_exists, \
    delete_current_user


@user_ns.route('', strict_slashes=False, endpoint='user_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(500, 'Internal Server Error')
class UserResource(Resource):

    @user_ns.response(200, 'Show the current user', user)
    @token_auth.login_required
    def get(self):
        """Show the user with the selected user_id"""
        return marshal(get_current_user().as_dict(), user), 200

    @user_ns.expect(modify_user, validate=True)
    @user_ns.response(204, 'User successfully modified')
    @user_ns.response(409, "Username already exists")
    @user_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self):
        """Update the current user"""
        json_data = request.get_json(force=True)
        if email_exists(json_data['email']):
            user_ns.abort(409, "Username already exists")
        edit_current_user(json_data)
        return '', 204

    @user_ns.response(204, 'User was successfully deleted')
    @token_auth.login_required
    def delete(self):
        """Delete the current user"""
        delete_current_user()
        return '', 204
