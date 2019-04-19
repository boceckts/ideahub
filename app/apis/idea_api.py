from datetime import datetime
from flask import request
from flask_restplus import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Idea
from app.utils.db_utils import expand_idea, expand_ideas

idea_ns = Namespace('ideas', description='Idea operations')

new_idea = idea_ns.model('New Idea', {
    'id': fields.Integer(readOnly=True, description='The idea\'s unique id'),
    'title': fields.String(readOnly=True, required=True, description='The idea\'s title'),
    'description': fields.String(readOnly=True, description='The idea\'s description'),
    'categories': fields.String(readOnly=True, description='The idea\'s categories'),
    'tags': fields.String(readOnly=True, description='The idea\'s tags')
})

idea = idea_ns.inherit('Idea', new_idea, {
    'created': fields.String(readOnly=True, description='The idea\'s creation date'),
    'modified': fields.String(readOnly=True, description='The idea\'s last modified date'),
    'author': fields.Integer(readOnly=True, requuired=True, description='The id of the idea\'s author')
})


@idea_ns.route('', strict_slashes=False)
@idea_ns.response(500, 'Internal Server Error')
class IdeasResource(Resource):

    @idea_ns.marshal_list_with(idea, code=200, description='List all ideas')
    def get(self):
        """List all ideas"""
        ideas = Idea.query.all()
        return expand_ideas(ideas), 200

    @idea_ns.expect(new_idea, 201, 'Idea created', validate=True)
    @idea_ns.response(400, 'Bad request')
    @idea_ns.response(409, 'Idea already exists')
    def post(self):
        """Create a new idea"""
        json_data = request.get_json(force=True)
        new_idea = Idea()
        new_idea.title = json_data['title']
        new_idea.description = json_data['description']
        new_idea.categories = json_data['categories']
        new_idea.tags = json_data['tags']
        db.session.add(new_idea)
        try:
            db.session.commit()
        except IntegrityError:
            idea_ns.abort(409, "Idea already exists")
        return "{}/{}".format(request.url, new_idea.id), 201

    @idea_ns.response(204, 'Ideas successfully deleted')
    def delete(self):
        """Delete all ideas"""
        db.session.query(Idea).delete()
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

    @idea_ns.expect(new_idea, 204, 'Idea was successfully modified', validate=True)
    @idea_ns.response(409, "Idea already exists")
    @idea_ns.response(400, 'Bad request')
    def put(self, idea_id):
        """Update the idea with the selected idea_id"""
        if Idea.query.get(idea_id) is None:
            idea_ns.abort(404, 'Idea not found')
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
    def delete(self, idea_id):
        """Delete the idea with the selected idea_id"""
        if Idea.query.get(idea_id) is None:
            idea_ns.abort(404, 'Idea not found')
        db.session.query(Idea).filter_by(id=idea_id).delete()
        db.session.commit()
        return '', 204
