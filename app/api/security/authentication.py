from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.models import User

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@basic_auth.error_handler
@token_auth.error_handler
def basic_auth_error():
    return jsonify({'error': 'Unauthorized access'})
