from flask import g
from flask_restplus import abort

from app.models.user import UserRole


def check_for_ownership(user_id):
    if g.current_user.id != user_id:
        abort(403, 'You are not allowed to access the resource')


def check_for_idea_ownership(idea):
    if g.current_user.id != idea.author.id:
        abort(403, 'You are not allowed to access the resource')


def check_for_admin_or_idea_ownership(idea):
    return is_admin() or check_for_idea_ownership(idea)


def check_for_vote_ownership(vote):
    if g.current_user.id != vote.user_id:
        abort(403, 'You are not allowed to access the resource')


def check_for_admin_or_vote_ownership(idea):
    return is_admin() or check_for_vote_ownership(idea)


def is_admin():
    return g.current_user.role == UserRole.admin
