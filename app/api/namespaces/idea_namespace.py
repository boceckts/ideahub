from flask_restplus import fields, Namespace

idea_ns = Namespace('ideas', description='Idea operations')

new_idea = idea_ns.model('New Idea', {
    'title': fields.String(required=True, description='The idea\'s title'),
    'description': fields.String(description='The idea\'s description'),
    'categories': fields.String(description='The idea\'s categories'),
    'tags': fields.String(description='The idea\'s tags')
})

public_idea = idea_ns.inherit('Public Idea', new_idea, {
    'id': fields.Integer(readonly=True, description='The idea\'s unique id'),
    'votes_url': fields.String(readonly=True, description='The url to the votes targeting this idea'),
    'score': fields.Integer(readonly=True, description='The sum of all the votes for this idea')
})

idea = idea_ns.inherit('Idea', public_idea, {
    'created': fields.String(readonly=True, description='The idea\'s creation date'),
    'modified': fields.String(readonly=True, description='The idea\'s last modified date'),
    'author': fields.Integer(readonly=True, requuired=True, description='The id of the idea\'s author'),
    'votes_count': fields.Integer(readonly=True, description='The number of votes that are targeted to this idea'),
    'upvotes': fields.Integer(readonly=True, description='The number of negative votes that are targeted to this idea'),
    'downvotes': fields.Integer(readonly=True, description='The number of positive votes that are targeted to this idea')
})
