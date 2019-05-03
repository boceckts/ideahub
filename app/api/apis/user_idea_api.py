from flask_restplus import Resource, marshal

from app import db
from app.api.namespaces import user_ns
from app.api.namespaces.idea_namespace import idea
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_ownership
from app.models import User
from app.utils import collection_as_dict


@user_ns.route('/<int:user_id>/ideas', strict_slashes=False, endpoint='user_ideas_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(403, 'Forbidden')
@user_ns.response(404, 'User not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeasResource(Resource):

    @user_ns.response(200, 'Show the ideas for the user with the selected id', [idea])
    @token_auth.login_required
    def get(self, user_id):
        """Show all ideas for the user with the selected id"""
        check_for_ownership(user_id)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return marshal(collection_as_dict(queried_user.ideas.all()), idea), 200

    @user_ns.response(204, 'Ideas successfully deleted')
    @token_auth.login_required
    def delete(self, user_id):
        """Delete all ideas for the user with the selected id"""
        check_for_ownership(user_id)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.ideas.delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
