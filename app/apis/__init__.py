from app import app
from flask_restplus import Api

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

api.init_app(app)
