from flask import g
from flask_restplus import Resource, marshal

from app.api.namespaces import user_ns
from app.api.namespaces.vote_namespace import vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import is_admin
from app.services.vote_service import delete_votes_for_user
from app.utils import collection_as_dict


@user_ns.route('/votes', strict_slashes=False, endpoint='user_votes_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(403, 'Forbidden')
@user_ns.response(500, 'Internal Server Error')
class UserVotesResource(Resource):

    @user_ns.response(200, 'Show the votes for the current user', [vote])
    @token_auth.login_required
    def get(self):
        """Show all votes for the current user"""
        if is_admin():
            user_ns.abort(403, 'Admin has no votes')
        return marshal(collection_as_dict(g.current_user.votes), vote), 200

    @user_ns.response(204, 'Votes successfully deleted')
    @token_auth.login_required
    def delete(self):
        """Delete all votes for the current user"""
        if is_admin():
            user_ns.abort(403, 'Admin has no votes')
        delete_votes_for_user(g.current_user.id)
        return '', 204
