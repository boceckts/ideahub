from datetime import datetime

from flask import request, g
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.namespaces import idea_ns
from app.api.namespaces.idea_namespace import idea, public_idea, new_idea
from app.api.namespaces.vote_namespace import vote
from app.api.security.authentication import token_auth
from app.api.security.authorization import check_for_idea_ownership
from app.models.idea import Idea
from app.utils.db_utils import expand_idea, expand_ideas, expand_votes


@idea_ns.route('', strict_slashes=False)
@idea_ns.response(401, 'Unauthorized')
@idea_ns.response(500, 'Internal Server Error')
class IdeasResource(Resource):

    @idea_ns.response(200, 'List all ideas', [public_idea])
    @token_auth.login_required
    def get(self):
        """List all ideas"""
        ideas = Idea.query.all()
        return marshal(expand_ideas(ideas), public_idea), 200

    @idea_ns.expect(new_idea, validate=True)
    @idea_ns.response(201, 'Idea successfully created', idea, headers={'location': 'The idea\'s location'})
    @idea_ns.response(400, 'Bad request')
    @idea_ns.response(409, 'Idea already exists')
    @token_auth.login_required
    def post(self):
        """Create a new idea for the current user"""
        json_data = request.get_json(force=True)
        future_idea = Idea()
        future_idea.title = json_data['title']
        future_idea.description = json_data['description']
        future_idea.categories = json_data['categories']
        future_idea.tags = json_data['tags']
        future_idea.author = g.current_user
        try:
            g.current_user.ideas.append(future_idea)
            db.session.commit()
        except IntegrityError:
            idea_ns.abort(409, "Idea already exists")
        return marshal(expand_idea(future_idea), idea), 201, {'Location': '{}/{}'.format(request.url, future_idea.id)}


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
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(queried_idea)
        return marshal(expand_idea(queried_idea), idea), 200

    @idea_ns.expect(new_idea, validate=True)
    @idea_ns.response(204, 'Idea successfully modified')
    @idea_ns.response(409, "Idea already exists")
    @idea_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self, idea_id):
        """Update the idea with the selected idea_id"""
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(queried_idea)
        json_data = request.get_json(force=True)
        try:
            db.session.query(Idea).filter_by(id=idea_id).update({
                Idea.title: json_data['title'],
                Idea.description: json_data['description'],
                Idea.categories: json_data['categories'],
                Idea.tags: json_data['tags'],
                Idea.modified: datetime.utcnow()
            })
            db.session.commit()
        except IntegrityError:
            idea_ns.abort(409, "Idea already exists")
        return '', 204

    @idea_ns.response(204, 'Idea was successfully deleted')
    @token_auth.login_required
    def delete(self, idea_id):
        """Delete the idea with the selected idea_id"""
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(queried_idea)
        db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
        db.session.commit()
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
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        check_for_idea_ownership(queried_idea)
        return marshal(expand_votes(queried_idea.votes), vote), 200
