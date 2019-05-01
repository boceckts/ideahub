from flask_restplus import Resource, marshal

from app import db
from app.api.namespaces.vote_namespace import vote, vote_ns, public_vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_vote_ownership
from app.models.vote import Vote
from app.utils.db_utils import expand_votes, expand_vote


@vote_ns.route('', strict_slashes=False)
@vote_ns.response(401, 'Unauthorized')
@vote_ns.response(500, 'Internal Server Error')
class VotesResource(Resource):

    @vote_ns.response(200, 'List all votes', [public_vote])
    @token_auth.login_required
    def get(self):
        """List all votes"""
        votes = Vote.query.all()
        return marshal(expand_votes(votes), public_vote), 200

    @vote_ns.response(204, 'Votes successfully deleted')
    @token_auth.login_required
    def delete(self):
        """Delete all votes"""
        db.session.query(Vote).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@vote_ns.route('/<int:vote_id>', strict_slashes=False)
@vote_ns.response(401, 'Unauthorized')
@vote_ns.response(404, 'Vote not found')
@vote_ns.response(500, 'Internal Server Error')
class VoteResource(Resource):

    @vote_ns.response(200, 'Show the selected vote', vote)
    @token_auth.login_required
    def get(self, vote_id):
        """Show the vote with the selected vote_id"""
        queried_vote = Vote.query.get(vote_id)
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        check_for_vote_ownership(queried_vote)
        return marshal(expand_vote(queried_vote), vote), 200

    @vote_ns.response(204, 'Vote was successfully deleted')
    @token_auth.login_required
    def delete(self, vote_id):
        """Delete the vote with the selected vote_id"""
        queried_vote = Vote.query.get(vote_id)
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        check_for_vote_ownership(queried_vote)
        db.session.query(Vote).filter_by(id=vote_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
