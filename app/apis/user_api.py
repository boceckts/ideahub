from datetime import datetime

from flask import request
from flask_restplus import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Idea
from app.utils.db_utils import expand_users, expand_user, expand_idea

user_ns = Namespace('users', description='User operations')

user = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The user\'s unique id'),
    'username': fields.String(readOnly=True, required=True, description='The user\'s unique username'),
    'name': fields.String(readOnly=True, description='The user\'s name'),
    'surname': fields.String(readOnly=True, description='The user\'s surname'),
    'email': fields.String(readOnly=True, required=True, description='The user\'s unique email address'),
    'ideas': fields.List(cls_or_instance=fields.Integer, readonly=True,
                         description='The ids of the ideas that the user created')
})

new_user = user_ns.inherit('New User', user, {
    'password': fields.String(readOnly=True, required=True, description='The user\'s password')
})

new_idea = user_ns.model('New Idea', {
    'id': fields.Integer(readOnly=True, description='The idea\'s unique id'),
    'title': fields.String(readOnly=True, required=True, description='The idea\'s title'),
    'description': fields.String(readOnly=True, description='The idea\'s description'),
    'categories': fields.String(readOnly=True, description='The idea\'s categories'),
    'tags': fields.String(readOnly=True, description='The idea\'s tags')
})

idea = user_ns.inherit('Idea', new_idea, {
    'created': fields.String(readOnly=True, description='The idea\'s creation date'),
    'modified': fields.String(readOnly=True, description='The idea\'s last modified date'),
    'author': fields.Integer(readOnly=True, requuired=True, description='The id of the idea\'s author')
})

new_vote = user_ns.model('New Vote', {
    'user_id': fields.Integer(readOnly=True, description='The user id of the user that issued the vote'),
    'idea_id': fields.Integer(readOnly=True, required=True, description='The idea id that the vote belongs to'),
    'value': fields.Integer(readOnly=True, description='The value of the vote')
})

vote = user_ns.inherit('Vote', new_vote, {
    'created': fields.DateTime(readOnly=True, description='The vote\'s creation date'),
    'modified': fields.DateTime(readOnly=True, description='The vote\'s last modified date')
})


@user_ns.route('', strict_slashes=False)
@user_ns.response(500, 'Internal Server Error')
class UsersResource(Resource):

    @user_ns.marshal_list_with(user, code=200, description='List all users')
    def get(self):
        """List all users"""
        queried_users = User.query.all()
        return expand_users(queried_users), 200

    @user_ns.expect(new_user, 201, 'User created', validate=True)
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'User already exists')
    def post(self):
        """Create a new user"""
        json_data = request.get_json(force=True)
        future_user = User()
        future_user.username = json_data['username']
        future_user.name = json_data['name']
        future_user.surname = json_data['surname']
        future_user.email = json_data['email']
        future_user.set_password(json_data['password'])
        db.session.add(future_user)
        try:
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "User already exists")
        return "{}/{}".format(request.url, new_user.id), 201

    @user_ns.response(204, 'Users successfully deleted')
    def delete(self):
        """Delete all users"""
        db.session.query(User).delete()
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>', strict_slashes=False)
@user_ns.response(404, 'User not found')
@user_ns.response(500, 'Internal Server Error')
class UserResource(Resource):

    @user_ns.marshal_with(user, code=200, description='Show the selected user')
    def get(self, user_id):
        """Show the user with the selected user_id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return expand_user(queried_user), 200

    @user_ns.expect(new_user, 204, 'User was successfully modified', validate=True)
    @user_ns.response(409, "Username already exists")
    @user_ns.response(400, 'Bad request')
    def put(self, user_id):
        """Update the user with the selected user_id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        json_data = request.get_json(force=True)
        new_user = User()
        new_user.set_password(json_data['password'])
        try:
            db.session.query(User).filter_by(id=user_id).update({
                User.username: json_data['username'],
                User.name: json_data['name'],
                User.surname: json_data['surname'],
                User.password_hash: new_user.password_hash
            })
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Username already exists")
        return '', 204

    @user_ns.response(204, 'User was successfully deleted')
    def delete(self, user_id):
        """Delete the user with the selected user_id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/ideas', strict_slashes=False)
@user_ns.response(404, 'User not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeasResource(Resource):

    @user_ns.marshal_with(idea, code=200, description='Show the ideas for the user with the selected id')
    def get(self, user_id):
        """Show all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        ideas = queried_user.ideas.all()
        return list(map(lambda idea: idea.as_dict(), ideas)), 200

    @user_ns.expect(new_idea, 201, 'Idea created', validate=True)
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'Idea already exists')
    def post(self, user_id):
        """Create a new idea for the user with the selected id"""
        json_data = request.get_json(force=True)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        new_idea = Idea()
        new_idea.title = json_data['title']
        new_idea.description = json_data['description']
        new_idea.categories = json_data['categories']
        new_idea.tags = json_data['tags']
        new_idea.author = queried_user
        try:
            queried_user.ideas.append(new_idea)
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Idea already exists")
        return "{}/{}".format(request.url, new_idea.id), 201

    @user_ns.response(204, 'Ideas successfully deleted')
    def delete(self, user_id):
        """Delete all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.ideas.delete()
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/ideas/<int:idea_id>', strict_slashes=False)
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeaResource(Resource):

    @user_ns.marshal_with(idea, code=200, description='Show the selected idea')
    def get(self, user_id, idea_id):
        """Show the idea with the selected idea_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        queried_idea = Idea.query.get(idea_id)
        if queried_idea is None:
            user_ns.abort(404, 'Idea not found')
        return expand_idea(queried_idea), 200

    @user_ns.expect(new_idea, 204, 'Idea was successfully modified', validate=True)
    @user_ns.response(409, "Idea already exists")
    @user_ns.response(400, 'Bad request')
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
    def delete(self, user_id, idea_id):
        """Delete the idea with the selected idea_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Idea.query.get(idea_id) is None:
            user_ns.abort(404, 'Idea not found')
        db.session.query(Idea).filter_by(id=idea_id).delete()
        db.session.commit()
        return '', 204
