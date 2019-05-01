from flask_restplus import fields, Namespace

user_ns = Namespace('users', description='User operations')

modify_user = user_ns.model('Modify User', {
    'username': fields.String(required=True, description='The user\'s unique username'),
    'name': fields.String(description='The user\'s name'),
    'surname': fields.String(description='The user\'s surname'),
    'email': fields.String(required=True, description='The user\'s unique email address')
})

new_user = user_ns.inherit('New User', modify_user, {
    'password': fields.String(required=True, description='The user\'s password')
})

public_user = user_ns.model('Public User', {
    'id': fields.Integer(readonly=True, description='The user\'s unique id'),
    'username': fields.String(readonly=True, required=True, description='The user\'s unique username'),
    'ideas_url': fields.String(readonly=True, description='The url to this user\'s ideas'),
    'votes_url': fields.String(readonly=True, description='The url to this user\'s votes')
})

user = user_ns.inherit('User', public_user, {
    'name': fields.String(readonly=True, description='The user\'s name'),
    'surname': fields.String(readonly=True, description='The user\'s surname'),
    'email': fields.String(readonly=True, required=True, description='The user\'s unique email address'),
    'ideas_count': fields.Integer(readonly=True, description='The number of ideas that the user created'),
    'votes_count': fields.Integer(readonly=True, description='The number of votes that the user issued')
})
