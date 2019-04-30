from flask_restplus import Resource

from app import db
from app.apis.namespaces import idea_ns
from app.apis.namespaces.ideas_namespace import idea
from app.apis.namespaces.votes_namespace import vote
from app.models.idea import Idea
from app.utils.db_utils import expand_idea, expand_ideas, expand_votes


@idea_ns.route('', strict_slashes=False)
@idea_ns.response(500, 'Internal Server Error')
class IdeasResource(Resource):

    @idea_ns.marshal_list_with(idea, code=200, description='List all ideas')
    def get(self):
        """List all ideas"""
        ideas = Idea.query.all()
        return expand_ideas(ideas), 200

    @idea_ns.response(204, 'Ideas successfully deleted')
    def delete(self):
        """Delete all ideas"""
        db.session.query(Idea).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@idea_ns.route('/<int:idea_id>', strict_slashes=False)
@idea_ns.response(404, 'Idea not found')
@idea_ns.response(500, 'Internal Server Error')
class IdeaResource(Resource):

    @idea_ns.marshal_with(idea, code=200, description='Show the selected idea')
    def get(self, idea_id):
        """Show the idea with the selected idea_id"""
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        return expand_idea(queried_idea), 200

    @idea_ns.response(204, 'Idea was successfully deleted')
    def delete(self, idea_id):
        """Delete the idea with the selected idea_id"""
        if Idea.query.get(idea_id) is None:
            idea_ns.abort(404, 'Idea not found')
        db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@idea_ns.route('/<int:idea_id>/votes', strict_slashes=False, endpoint='idea_votes_ep')
@idea_ns.response(404, 'Resource not found')
@idea_ns.response(500, 'Internal Server Error')
class IdeaVotesResource(Resource):

    @idea_ns.marshal_with(vote, code=200, description='Show the votes for the selected idea')
    def get(self, idea_id):
        """Show all votes that are targeted to the idea with the selected id"""
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            idea_ns.abort(404, 'Idea not found')
        return expand_votes(queried_idea.votes), 200
