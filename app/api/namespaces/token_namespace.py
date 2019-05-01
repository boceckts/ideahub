from flask_restplus import Namespace, fields

token_ns = Namespace('token', description='Token operations')

token = token_ns.model('Token', {
    'token': fields.String(readOnly=True, description='An authentication token for a logged in user')
})
