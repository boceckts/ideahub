from flask_restplus import fields, Namespace

vote_ns = Namespace('votes', description='Vote operations')

public_vote = vote_ns.model('Public Vote', {
    'id': fields.Integer(readonly=True, description='The vote\'s autogenerated id'),
    'value': fields.Integer(readonly=True, description='The value of the vote')
})

vote = vote_ns.inherit('Vote', public_vote, {
    'owner': fields.Integer(readonly=True, required=True, description='The id of the user that issued the vote'),
    'target': fields.Integer(readonly=True, required=True, description='The id of the idea that the vote belongs to'),
    'created': fields.DateTime(readonly=True, description='The vote\'s creation date'),
    'modified': fields.DateTime(readonly=True, description='The vote\'s last modified date')
})

new_vote = vote_ns.model('New Vote', {
    'target': fields.Integer(required=True, description='The idea id that the vote belongs to'),
    'value': fields.Integer(required=True, description='The value of the vote')
})

modify_vote = vote_ns.model('Modify Vote', {
    'value': fields.Integer(required=True, description='The value of the vote')
})
