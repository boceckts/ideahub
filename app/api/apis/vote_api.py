from flask_restplus import Resource

from app import db
from app.models.vote import Vote
from app.utils.db_utils import expand_votes, expand_vote
from app.api.namespaces import *
from app.api.namespaces.vote_namespace import vote


@vote_ns.route('', strict_slashes=False)
@vote_ns.response(500, 'Internal Server Error')
class VotesResource(Resource):

    @vote_ns.marshal_list_with(vote, code=200, description='List all votes')
    def get(self):
        """List all votes"""
        votes = Vote.query.all()
        return expand_votes(votes), 200

    @vote_ns.response(204, 'Votes successfully deleted')
    def delete(self):
        """Delete all votes"""
        db.session.query(Vote).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@vote_ns.route('/<int:vote_id>', strict_slashes=False)
@vote_ns.response(404, 'Vote not found')
@vote_ns.response(500, 'Internal Server Error')
class IdeaResource(Resource):

    @vote_ns.marshal_with(vote, code=200, description='Show the selected vote')
    def get(self, vote_id):
        """Show the vote with the selected vote_id"""
        queried_vote = db.session.query(Vote).filter_by(id=vote_id).first()
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        return expand_vote(queried_vote), 200

    @vote_ns.response(204, 'Vote was successfully deleted')
    def delete(self, vote_id):
        """Delete the vote with the selected vote_id"""
        if Vote.query.get(vote_id) is None:
            vote_ns.abort(404, 'Vote not found')
        db.session.query(Vote).filter_by(id=vote_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
