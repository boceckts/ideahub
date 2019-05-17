from flask import request, g
from flask_restplus import Resource, marshal

from app.api.namespaces.user_namespaces import user_ns, user, modify_user
from app.api.security.authentication import token_auth
from app.api.security.authorization import is_admin
from app.services.user_service import edit_user_by_json, email_exists, \
    delete_user_by_id


@user_ns.route('', strict_slashes=False, endpoint='user_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(500, 'Internal Server Error')
class UserResource(Resource):

    @user_ns.response(200, 'Show the current user', user)
    @token_auth.login_required
    def get(self):
        """Show the user with the selected user_id"""
        return marshal(g.current_user.as_dict(), user), 200

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
        edit_user_by_json(g.current_user.id, json_data)
        return '', 204

    @user_ns.response(204, 'User was successfully deleted')
    @user_ns.response(403, 'Forbidden')
    @token_auth.login_required
    def delete(self):
        """Delete the current user"""
        if is_admin():
            user_ns.abort(403, 'Admin user can not be deleted')
        delete_user_by_id(g.current_user)
        return '', 204
