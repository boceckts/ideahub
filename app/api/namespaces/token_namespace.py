from flask_restplus import Namespace, fields

token_ns = Namespace('token', description='Token operations')

token = token_ns.model('Token', {
    'token': fields.String(readonly=True, description='An authentication token for a logged in user'),
    'expires_on': fields.DateTime(readonly=True, description='The expiry date of the token')
})
