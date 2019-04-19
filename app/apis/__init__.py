from app import app
from flask_restplus import Api

from app.apis.idea_api import idea_ns
from app.apis.user_api import user_ns
from app.apis.vote_api import vote_ns

api = Api(
    title='IdeaHub API',
    description='This is the Application Programming Interface (API) specification for the IdeaHub web application.',
    version='1.0',
    contact='IdeaHub',
    contact_url='/',
    ordered=True,
    doc='/api/v1/docs',
    prefix='/api/v1'
)

api.add_namespace(user_ns)
api.add_namespace(idea_ns)
api.add_namespace(vote_ns)

api.init_app(app)
