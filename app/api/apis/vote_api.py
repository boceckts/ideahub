from datetime import datetime

from flask import request, g
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.namespaces.vote_namespace import vote, vote_ns, public_vote, new_vote, modify_vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_vote_ownership
from app.models import Idea
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

    @vote_ns.expect(new_vote, validate=True)
    @vote_ns.response(201, 'Vote successfully created', vote, headers={'location': 'The vote\'s location'})
    @vote_ns.response(400, 'Bad request')
    @vote_ns.response(409, 'Conflict')
    @token_auth.login_required
    def post(self):
        """Create a new idea for the current user"""
        json_data = request.get_json(force=True)
        idea_id = json_data['target']
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            vote_ns.abort(409, 'Target not found')
        existing_vote = Vote.query.filter_by(user_id=g.current_user.id, idea_id=idea_id).first()
        if existing_vote is not None:
            vote_ns.abort(409, 'Vote already exists')
        future_vote = Vote()
        future_vote.value = json_data['value']
        future_vote.target = queried_idea
        future_vote.owner = g.current_user
        try:
            db.session.add(future_vote)
            db.session.commit()
        except IntegrityError:
            vote_ns.abort(409, "Vote already exists")
        return marshal(expand_vote(future_vote), vote), 201, {'Location': '{}/{}'.format(request.url, future_vote.id)}

    @vote_ns.response(204, 'Votes successfully deleted')
    @token_auth.login_required
    def delete(self):
        """Delete all votes"""
        db.session.query(Vote).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@vote_ns.route('/<int:vote_id>', strict_slashes=False)
@vote_ns.response(401, 'Unauthorized')
@vote_ns.response(403, 'Forbidden')
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

    @vote_ns.expect(modify_vote, validate=True)
    @vote_ns.response(204, 'Vote successfully modified')
    @vote_ns.response(409, "Vote already exists")
    @vote_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self, vote_id):
        """Update the vote with the selected vote_id"""
        queried_vote = Vote.query.get(vote_id)
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        check_for_vote_ownership(queried_vote)
        json_data = request.get_json(force=True)
        try:
            db.session.query(Vote).filter_by(id=vote_id).update({
                Vote.value: json_data['value'],
                Vote.modified: datetime.utcnow()
            })
            db.session.commit()
        except IntegrityError:
            vote_ns.abort(409, "Vote already exists")
        return '', 204

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
