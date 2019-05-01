from flask import g
from flask_restplus import abort


def check_for_ownership(id):
    if g.current_user.id != id:
        abort(403, 'You are not allowed to access the resource')


def check_for_idea_ownership(idea):
    if g.current_user.id != idea.author.id:
        abort(403, 'You are not allowed to access the resource')


def check_for_vote_ownership(vote):
    if g.current_user.id != vote.owner:
        abort(403, 'You are not allowed to access the resource')
