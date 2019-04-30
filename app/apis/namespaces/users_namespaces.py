from flask_restplus import fields

from app.apis.namespaces import user_ns

modify_user = user_ns.model('Modify User', {
    'id': fields.Integer(readOnly=True, description='The user\'s unique id'),
    'username': fields.String(readOnly=True, required=True, description='The user\'s unique username'),
    'name': fields.String(readOnly=True, description='The user\'s name'),
    'surname': fields.String(readOnly=True, description='The user\'s surname'),
    'email': fields.String(readOnly=True, required=True, description='The user\'s unique email address')
})

new_user = user_ns.inherit('New User', modify_user, {
    'password': fields.String(readOnly=True, required=True, description='The user\'s password')
})

user = user_ns.inherit('User', modify_user, {
    'id': fields.Integer(readOnly=True, description='The user\'s unique id'),
    'username': fields.String(readOnly=True, required=True, description='The user\'s unique username'),
    'name': fields.String(readOnly=True, description='The user\'s name'),
    'surname': fields.String(readOnly=True, description='The user\'s surname'),
    'email': fields.String(readOnly=True, required=True, description='The user\'s unique email address'),
    'ideas_count': fields.Integer(readonly=True, description='The number of ideas that the user created'),
    'votes_count': fields.Integer(readonly=True, description='The number of votes that the user issued'),
    'ideas_url': fields.String(readonly=True, description='The url to this user\'s ideas'),
    'votes_url': fields.String(readonly=True, description='The url to this user\'s votes')
})
