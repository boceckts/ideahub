from flask import request, g
from flask_restplus import Resource, marshal

from app.api.namespaces import idea_ns
from app.api.namespaces.idea_namespace import idea, public_idea, new_idea
from app.api.namespaces.vote_namespace import vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_idea_ownership
from app.models.idea import Idea
from app.services.idea_service import get_all_ideas, get_idea, idea_exists, idea_title_exists, \
    delete_idea_by_id, save_idea, edit_idea_by_json
from app.utils import collection_as_dict


@idea_ns.route('', strict_slashes=False)
@idea_ns.response(401, 'Unauthorized')
@idea_ns.response(500, 'Internal Server Error')
class IdeasResource(Resource):

    @idea_ns.response(200, 'List all ideas', [public_idea])
    @token_auth.login_required
    def get(self):
        """List all ideas"""
        return marshal(collection_as_dict(get_all_ideas()), public_idea), 200

    @idea_ns.expect(new_idea, validate=True)
    @idea_ns.response(201, 'Idea successfully created', idea, headers={'location': 'The idea\'s location'})
    @idea_ns.response(400, 'Bad request')
    @idea_ns.response(409, 'Idea already exists')
    @token_auth.login_required
    def post(self):
        """Create a new idea for the current user"""
        json_data = request.get_json(force=True)
        if idea_title_exists(json_data['title']):
            idea_ns.abort(409, "Idea already exists")
        future_idea = Idea()
        future_idea.title = json_data['title']
        future_idea.description = json_data['description']
        future_idea.category = json_data['category']
        future_idea.tags = json_data['tags']
        future_idea.author = g.current_user
        save_idea(future_idea)
        return marshal(future_idea.as_dict(), idea), 201, {'Location': '{}/{}'.format(request.url, future_idea.id)}


@idea_ns.route('/<int:idea_id>', strict_slashes=False)
@idea_ns.response(401, 'Unauthorized')
@idea_ns.response(403, 'Forbidden')
@idea_ns.response(404, 'Idea not found')
@idea_ns.response(500, 'Internal Server Error')
class IdeaResource(Resource):

    @idea_ns.response(200, 'Show the selected idea', idea)
    @token_auth.login_required
    def get(self, idea_id):
        """Show the idea with the selected idea_id"""
        queried_idea = get_idea(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(queried_idea)
        return marshal(queried_idea.as_dict(), idea), 200

    @idea_ns.expect(new_idea, validate=True)
    @idea_ns.response(204, 'Idea successfully modified')
    @idea_ns.response(409, "Idea already exists")
    @idea_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self, idea_id):
        """Update the idea with the selected idea_id"""
        if not idea_exists(idea_id):
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(get_idea(idea_id))
        json_data = request.get_json(force=True)
        if idea_title_exists(json_data['title']):
            idea_ns.abort(409, "Idea already exists")
        edit_idea_by_json(idea_id, json_data)
        return '', 204

    @idea_ns.response(204, 'Idea was successfully deleted')
    @token_auth.login_required
    def delete(self, idea_id):
        """Delete the idea with the selected idea_id"""
        if not idea_exists(idea_id):
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(get_idea(idea_id))
        delete_idea_by_id(idea_id)
        return '', 204


@idea_ns.route('/<int:idea_id>/votes', strict_slashes=False, endpoint='idea_votes_ep')
@idea_ns.response(401, 'Unauthorized')
@idea_ns.response(403, 'Forbidden')
@idea_ns.response(404, 'Resource not found')
@idea_ns.response(500, 'Internal Server Error')
class IdeaVotesResource(Resource):

    @idea_ns.response(200, 'Show the votes for the selected idea', [vote])
    @token_auth.login_required
    def get(self, idea_id):
        """Show all votes that are targeted to the idea with the selected id"""
        if not idea_exists(idea_id):
            idea_ns.abort(404, 'Idea not found')
        queried_idea = get_idea(idea_id)
        check_for_idea_ownership(queried_idea)
        return marshal(collection_as_dict(queried_idea.votes), vote), 200
