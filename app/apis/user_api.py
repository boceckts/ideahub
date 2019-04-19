from flask import request
from flask_restplus import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User


user_ns = Namespace('users', description='User operations')

user = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The user\'s unique id'),
    'username': fields.String(readOnly=True, required=True, description='The user\'s unique username'),
    'name': fields.String(readOnly=True, description='The user\'s name'),
    'surname': fields.String(readOnly=True, description='The user\'s surname'),
    'email': fields.String(readOnly=True, required=True, description='The user\'s unique email address')
})

new_user = user_ns.inherit('New User', user, {
    'password': fields.String(readOnly=True, required=True, description='The user\'s password')
})


@user_ns.route('', strict_slashes=False)
@user_ns.response(500, 'Internal Server Error')
class UsersResource(Resource):

    @user_ns.marshal_list_with(user, code=200, description='List all users')
    def get(self):
        """List all users"""
        users = User.query.all()
        return list(map(lambda user: user.as_dict(), users)), 200

    @user_ns.expect(new_user, 201, 'User created', validate=True)
    @user_ns.response(400, 'Bad request')
    @user_ns.response(409, 'User already exists')
    def post(self):
        """Create a new user"""
        json_data = request.get_json(force=True)
        new_user = User()
        new_user.username = json_data['username']
        new_user.name = json_data['name']
        new_user.surname = json_data['surname']
        new_user.email = json_data['email']
        new_user.set_password(json_data['password'])
        db.session.add(new_user)
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
        return queried_user.as_dict(), 200

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
