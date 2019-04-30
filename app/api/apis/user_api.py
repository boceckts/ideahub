from flask import request
from flask_restplus import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.namespaces.user_namespaces import user_ns, user, new_user
from app.models import User
from app.utils.db_utils import expand_users, expand_user


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
