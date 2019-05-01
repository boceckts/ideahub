from flask_restplus import Resource, marshal

from app import db
from app.api.namespaces import user_ns
from app.api.namespaces.vote_namespace import vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_ownership
from app.models import User
from app.utils.db_utils import expand_votes


@user_ns.route('/<int:user_id>/votes', strict_slashes=False, endpoint='user_votes_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(403, 'Forbidden')
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserVotesResource(Resource):

    @user_ns.response(200, 'Show the votes for the user with the selected user id', [vote])
    @token_auth.login_required
    def get(self, user_id):
        """Show all votes for the user with the selected id"""
        check_for_ownership(user_id)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return marshal(expand_votes(queried_user.votes), vote), 200

    @user_ns.response(204, 'Votes successfully deleted')
    @token_auth.login_required
    def delete(self, user_id):
        """Delete all votes for the user with the selected user"""
        check_for_ownership(user_id)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.votes.delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
