from flask_restplus import Resource, Namespace, fields

from app import db
from app.models import Vote

vote_ns = Namespace('votes', description='Vote operations')

vote = vote_ns.model('New Vote', {
    'user_id': fields.Integer(readOnly=True, description='The user id of the user that issued the vote'),
    'idea_id': fields.Integer(readOnly=True, required=True, description='The idea id that the vote belongs to'),
    'value': fields.Integer(readOnly=True, description='The value of the vote'),
    'created': fields.DateTime(readOnly=True, description='The vote\'s creation date'),
    'modified': fields.DateTime(readOnly=True, description='The vote\'s last modified date')
})


@vote_ns.route('', strict_slashes=False)
@vote_ns.response(500, 'Internal Server Error')
class VotesResource(Resource):

    @vote_ns.marshal_list_with(vote, code=200, description='List all votes')
    def get(self):
        """List all votes"""
        votes = Vote.query.all()
        return list(map(lambda vote: vote.as_dict(), votes)), 200

    @vote_ns.response(204, 'Votes successfully deleted')
    def delete(self):
        """Delete all votes"""
        db.session.query(Vote).delete()
        db.session.commit()
        return '', 204
