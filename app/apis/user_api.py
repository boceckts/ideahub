from datetime import datetime

from flask import request
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.apis.namespaces import user_ns
from app.apis.namespaces.ideas_namespace import idea, new_idea
from app.apis.namespaces.users_namespaces import user, new_user
from app.apis.namespaces.votes_namespace import vote, new_vote, modify_vote
from app.models import User, Idea, Vote
from app.utils.db_utils import expand_users, expand_user, expand_idea, expand_votes, expand_ideas, expand_vote


@user_ns.route('', strict_slashes=False, endpoint='users_ep')
@user_ns.response(500, 'Internal Server Error')
class UsersResource(Resource):

    @user_ns.marshal_list_with(user, code=200, description='List all users')
    def get(self):
        """List all users"""
        queried_users = User.query.all()
        return expand_users(queried_users), 200

    @user_ns.expect(new_user, validate=True)
    @user_ns.response(201, 'User successfully created', user, headers={'location': 'The user\'s location'})
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
        return marshal(expand_user(future_user), user), 201, {'Location': '{}/{}'.format(request.url, future_user.id)}

    @user_ns.response(204, 'Users successfully deleted')
    def delete(self):
        """Delete all users"""
        db.session.query(User).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>', strict_slashes=False, endpoint='user_ep')
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

    @user_ns.expect(new_user, validate=True)
    @user_ns.response(204, 'User successfully modified')
    @user_ns.response(409, "Username already exists")
    @user_ns.response(400, 'Bad request')
    def put(self, user_id):
        """Update the user with the selected user_id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        json_data = request.get_json(force=True)
        temp_user = User()
        temp_user.set_password(json_data['password'])
        try:
            db.session.query(User).filter_by(id=user_id).update({
                User.username: json_data['username'],
                User.name: json_data['name'],
                User.surname: json_data['surname'],
                User.password_hash: temp_user.password_hash
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
        db.session.query(User).filter_by(id=user_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/ideas', strict_slashes=False, endpoint='user_ideas_ep')
@user_ns.response(404, 'User not found')
@user_ns.response(500, 'Internal Server Error')
class UserIdeasResource(Resource):

    @user_ns.marshal_with(idea, code=200, description='Show the ideas for the user with the selected id')
    def get(self, user_id):
        """Show all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return expand_ideas(queried_user.ideas.all()), 200

    @user_ns.expect(new_idea, validate=True)
    @user_ns.response(201, 'Idea successfully created', idea, headers={'location': 'The idea\'s location'})
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'Idea already exists')
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
    def delete(self, user_id):
        """Delete all ideas for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.ideas.delete(synchronize_session='fetch')
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

    @user_ns.expect(new_idea, validate=True)
    @user_ns.response(204, 'Idea successfully modified')
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
        db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/votes', strict_slashes=False, endpoint='user_votes_ep')
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserVotesResource(Resource):

    @user_ns.marshal_with(vote, code=200, description='Show the votes for the user with the selected user id')
    def get(self, user_id):
        """Show all votes for the user with the selected id"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        return expand_votes(queried_user.votes), 200

    @user_ns.expect(new_vote, validate=True)
    @user_ns.response(201, 'Vote successfully created', vote, headers={'location': 'The vote\'s location'})
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'Vote already exists')
    def post(self, user_id):
        """Create a new idea for the user with the selected id"""
        json_data = request.get_json(force=True)
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        future_vote = Vote()
        future_vote.value = json_data['value']
        queried_idea = Idea.query.get(json_data['target'])
        if queried_idea is None:
            user_ns.abort(409, 'Target not found')
        future_vote.target = queried_idea
        future_vote.owner = queried_user
        try:
            db.session.add(future_vote)
            db.session.commit()
        except IntegrityError:
            user_ns.abort(409, "Vote already exists")
        return marshal(expand_vote(future_vote), vote), 201, {'Location': '{}/{}'.format(request.url, future_vote.id)}

    @user_ns.response(204, 'Votes successfully deleted')
    def delete(self, user_id):
        """Delete all votes for the user with the selected user"""
        queried_user = User.query.get(user_id)
        if queried_user is None:
            user_ns.abort(404, 'User not found')
        queried_user.votes.delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204


@user_ns.route('/<int:user_id>/votes/<int:vote_id>', strict_slashes=False)
@user_ns.response(404, 'Resource not found')
@user_ns.response(500, 'Internal Server Error')
class UserVoteResource(Resource):

    @user_ns.marshal_with(vote, code=200, description='Show the selected vote')
    def get(self, user_id, vote_id):
        """Show the vote with the selected vote_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        queried_vote = Vote.query.get(vote_id)
        if queried_vote is None:
            user_ns.abort(404, 'Vote not found')
        return expand_vote(queried_vote), 200

    @user_ns.expect(modify_vote, validate=True)
    @user_ns.response(204, 'Vote successfully modified')
    @user_ns.response(409, "Vote already exists")
    @user_ns.response(400, 'Bad request')
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
    def delete(self, user_id, vote_id):
        """Delete the vote with the selected vote_id of the user with the selected user id"""
        if User.query.get(user_id) is None:
            user_ns.abort(404, 'User not found')
        if Vote.query.get(vote_id) is None:
            user_ns.abort(404, 'Vote not found')
        db.session.query(Vote).filter_by(id=vote_id).delete(synchronize_session='fetch')
        db.session.commit()
        return '', 204
