from flask import g
from flask_restplus import abort


def check_for_ownership(id):
    if g.current_user.id != id:
        abort(403, 'You are not allowed to access the resource')
