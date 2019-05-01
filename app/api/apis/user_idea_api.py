from datetime import datetime

from flask import request
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.namespaces import user_ns
from app.api.namespaces.idea_namespace import idea, new_idea
from app.api.security.authentication import token_auth
from app.models import User, Idea
from app.utils.db_utils import expand_idea, expand_ideas


@user_ns.route('/<int:user_id>/ideas', strict_slashes=False, endpoint='user_ideas_ep')
@user_ns.response(401, 'Unauthorized')
@user_ns.response(404, 'User not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeasResource(Resource):

    @user_ns.response(200, 'Show the ideas for the user with the selected id', [idea])
    @token_auth.login_required
    def get(self, user_id):
        """Show all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return marshal(expand_ideas(queried_user.ideas.all()), idea), 200

    @user_ns.expect(new_idea, validate=True)
    @user_ns.response(201, 'Idea successfully created', idea, headers={'location': 'The idea\'s location'})
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'Idea already exists')
    @token_auth.login_required
    def post(self, user_id):
        """Create a new idea for the user with the selected id"""
        json_data = request.get_json(force=True)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        future_idea = Idea()
        future_idea.title = json_data['title']
        future_idea.description = json_data['description']
        future_idea.categories = json_data['categories']
        future_idea.tags = json_data['tags']
        future_idea.author = queried_user
        try:
            queried_user.ideas.append(future_idea)
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Idea already exists")
        return marshal(expand_idea(future_idea), idea), 201, {'Location': '{}/{}'.format(request.url, future_idea.id)}

    @user_ns.response(204, 'Ideas successfully deleted')
    @token_auth.login_required
    def delete(self, user_id):
        """Delete all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.ideas.delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/ideas/<int:idea_id>', strict_slashes=False)
@user_ns.response(401, 'Unauthorized')
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeaResource(Resource):

    @user_ns.response(200, 'Show the selected idea', idea)
    @token_auth.login_required
    def get(self, user_id, idea_id):
        """Show the idea with the selected idea_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            user_ns.abort(404, 'Idea not found')
        return marshal(expand_idea(queried_idea), idea), 200

    @user_ns.expect(new_idea, validate=True)
    @user_ns.response(204, 'Idea successfully modified')
    @user_ns.response(409, "Idea already exists")
    @user_ns.response(400, 'Bad request')
    @token_auth.login_required
    def put(self, user_id, idea_id):
        """Update the idea with the selected idea_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Idea.query.get(idea_id) is None:
            user_ns.abort(404, 'Idea not found')
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
            user_ns.abort(409, "Idea already exists")
        return '', 204

    @user_ns.response(204, 'Idea was successfully deleted')
    @token_auth.login_required
    def delete(self, user_id, idea_id):
        """Delete the idea with the selected idea_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Idea.query.get(idea_id) is None:
            user_ns.abort(404, 'Idea not found')
        db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
