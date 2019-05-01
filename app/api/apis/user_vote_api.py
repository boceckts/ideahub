from datetime import datetime

from flask import request
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.namespaces import user_ns
from app.api.namespaces.vote_namespace import vote, new_vote, modify_vote
from app.api.security.authentication import token_auth
from app.models import User, Idea, Vote
from app.utils.db_utils import expand_votes, expand_vote


@user_ns.route('/<int:user_id>/votes', strict_slashes=False, endpoint='user_votes_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserVotesResource(Resource):

    @user_ns.response(200, 'Show the votes for the user with the selected user id', [vote])
    @token_auth.login_required
    def get(self, user_id):
        """Show all votes for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return marshal(expand_votes(queried_user.votes), vote), 200

    @user_ns.expect(new_vote, validate=True)
    @user_ns.response(201, 'Vote successfully created', vote, headers={'location': 'The vote\'s location'})
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'Conflict')
    @token_auth.login_required
    def post(self, user_id):
        """Create a new idea for the user with the selected id"""
        json_data = request.get_json(force=True)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        idea_id = json_data['target']
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            user_ns.abort(409, 'Target not found')
        existing_vote = Vote.query.filter_by(user_id=user_id, idea_id=idea_id).first()
        if existing_vote is not None:
            user_ns.abort(409, 'Vote already exists')
        future_vote = Vote()
        future_vote.value = json_data['value']
        future_vote.target = queried_idea
        future_vote.owner = queried_user
        try:
            db.session.add(future_vote)
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Vote already exists")
        return marshal(expand_vote(future_vote), vote), 201, {'Location': '{}/{}'.format(request.url, future_vote.id)}

    @user_ns.response(204, 'Votes successfully deleted')
    @token_auth.login_required
    def delete(self, user_id):
        """Delete all votes for the user with the selected user"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.votes.delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/votes/<int:vote_id>', strict_slashes=False)
@user_ns.response(401, 'Unauthorized')
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserVoteResource(Resource):

    @user_ns.response(200, 'Show the selected vote', vote)
    @token_auth.login_required
    def get(self, user_id, vote_id):
        """Show the vote with the selected vote_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        queried_vote = Vote.query.get(vote_id)
        if queried_vote is None:
            user_ns.abort(404, 'Vote not found')
        return marshal(expand_vote(queried_vote), vote), 200

    @user_ns.expect(modify_vote, validate=True)
    @user_ns.response(204, 'Vote successfully modified')
    @user_ns.response(409, "Vote already exists")
    @user_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self, user_id, vote_id):
        """Update the vote with the selected vote_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Vote.query.get(vote_id) is None:
            user_ns.abort(404, 'Vote not found')
        json_data = request.get_json(force=True)
        try:
            db.session.query(Vote).filter_by(id=vote_id).update({
                Vote.value: json_data['value'],
                Vote.modified: datetime.utcnow()
            })
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Vote already exists")
        return '', 204

    @user_ns.response(204, 'Vote was successfully deleted')
    @token_auth.login_required
    def delete(self, user_id, vote_id):
        """Delete the vote with the selected vote_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Vote.query.get(vote_id) is None:
            user_ns.abort(404, 'Vote not found')
        db.session.query(Vote).filter_by(id=vote_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
