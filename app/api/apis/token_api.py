from flask_restplus import Resource, marshal

from app import db
from app.api.namespaces.token_namespace import token_ns, token
from app.api.security.authentication import basic_auth, token_auth
from app.services.user_service import get_current_user


@token_ns.route('', strict_slashes=False)
@token_ns.response(401, 'Unauthorized')
@token_ns.response(500, 'Internal Server Error')
class TokensResource(Resource):

    @token_ns.response(200, 'Token successfully generated')
    @token_ns.doc(security='Basic Auth')
    @basic_auth.login_required
    def post(self):
        """Generate a new bearer token"""
        get_current_user().generate_auth_token()
        db.session.commit()
        token_obj = {'token': get_current_user().token,
                     'expires_on': get_current_user().token_expiration}
        return marshal(token_obj, token), 200

    @token_ns.response(204, 'Token successfully revoked')
    @token_auth.login_required
    def delete(self):
        """Revoke a token"""
        get_current_user().revoke_token()
        db.session.commit()
        return '', 204
