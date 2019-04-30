from flask_restplus import fields

from app.apis.namespaces import idea_ns

new_idea = idea_ns.model('New Idea', {
    'id': fields.Integer(readOnly=True, description='The idea\'s unique id'),
    'title': fields.String(readOnly=True, required=True, description='The idea\'s title'),
    'description': fields.String(readOnly=True, description='The idea\'s description'),
    'categories': fields.String(readOnly=True, description='The idea\'s categories'),
    'tags': fields.String(readOnly=True, description='The idea\'s tags')
})

idea = idea_ns.inherit('Idea', new_idea, {
    'created': fields.String(readOnly=True, description='The idea\'s creation date'),
    'modified': fields.String(readOnly=True, description='The idea\'s last modified date'),
    'author': fields.Integer(readOnly=True, requuired=True, description='The id of the idea\'s author'),
    'votes_count': fields.Integer(readonly=True, description='The number of votes that are targeted to this idea'),
    'votes_url': fields.String(readonly=True, description='The url to the votes targeting this idea')
})
