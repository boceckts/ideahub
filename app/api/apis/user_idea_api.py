from flask import g
from flask_restplus import Resource, marshal

from app.api.namespaces import user_ns
from app.api.namespaces.idea_namespace import idea
from app.api.security.authentication import token_auth
from app.api.security.authorization import is_admin
from app.services.idea_service import delete_ideas_for_user
from app.utils import collection_as_dict


@user_ns.route('/ideas', strict_slashes=False, endpoint='user_ideas_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(403, 'Forbidden')
@user_ns.response(500, 'Internal Server Error')
class UserIdeasResource(Resource):

    @user_ns.response(200, 'Show the ideas for the current user', [idea])
    @token_auth.login_required
    def get(self):
        """Show all ideas for the current user"""
        if is_admin():
            user_ns.abort(403, 'Admin has no ideas')
        return marshal(collection_as_dict(g.current_user.ideas), idea), 200

    @user_ns.response(204, 'Ideas successfully deleted')
    @token_auth.login_required
    def delete(self):
        """Delete all ideas for the current user"""
        if is_admin():
            user_ns.abort(403, 'Admin has no ideas')
        delete_ideas_for_user(g.current_user.id)
        return '', 204
