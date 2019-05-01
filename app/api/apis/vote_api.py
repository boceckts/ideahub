from flask import request, g
from flask_restplus import Resource, marshal

from app.api.namespaces.vote_namespace import vote, vote_ns, public_vote, new_vote, modify_vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_vote_ownership
from app.models.vote import Vote
from app.services.idea_service import idea_exists, get_idea
from app.services.vote_service import get_all_votes, save_vote, vote_exists, delete_vote_by_id, get_vote_by_id, \
    edit_vote
from app.utils.db_utils import expand_votes, expand_vote


@vote_ns.route('', strict_slashes=False)
@vote_ns.response(401, 'Unauthorized')
@vote_ns.response(500, 'Internal Server Error')
class VotesResource(Resource):

    @vote_ns.response(200, 'List all votes', [public_vote])
    @token_auth.login_required
    def get(self):
        """List all votes"""
        return marshal(expand_votes(get_all_votes()), public_vote), 200

    @vote_ns.expect(new_vote, validate=True)
    @vote_ns.response(201, 'Vote successfully created', vote, headers={'location': 'The vote\'s location'})
    @vote_ns.response(400, 'Bad request')
    @vote_ns.response(409, 'Conflict')
    @token_auth.login_required
    def post(self):
        """Create a new vote for the current user"""
        json_data = request.get_json(force=True)
        idea_id = json_data['target']
        if idea_exists(idea_id) is None:
            vote_ns.abort(409, 'Target not found')
        if vote_exists(g.current_user.id, idea_id):
            vote_ns.abort(409, 'Vote already exists')
        future_vote = Vote(owner=g.current_user,
                           target=get_idea(idea_id),
                           value=request.form.get('value'))
        save_vote(future_vote)
        return marshal(expand_vote(future_vote), vote), 201, {'Location': '{}/{}'.format(request.url, future_vote.id)}


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
        queried_vote = get_vote_by_id(vote_id)
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
        queried_vote = get_vote_by_id(vote_id)
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        check_for_vote_ownership(queried_vote)
        json_data = request.get_json(force=True)
        edit_vote(vote_id, json_data['value'])
        return '', 204

    @vote_ns.response(204, 'Vote was successfully deleted')
    @token_auth.login_required
    def delete(self, vote_id):
        """Delete the vote with the selected vote_id"""
        queried_vote = get_vote_by_id(vote_id)
        if queried_vote is None:
            vote_ns.abort(404, 'Vote not found')
        check_for_vote_ownership(queried_vote)
        delete_vote_by_id(vote_id)
        return '', 204
