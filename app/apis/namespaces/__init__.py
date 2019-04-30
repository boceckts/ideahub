from flask_restplus import Namespace

user_ns = Namespace('users', description='User operations')
idea_ns = Namespace('ideas', description='Idea operations')
vote_ns = Namespace('votes', description='Vote operations')
