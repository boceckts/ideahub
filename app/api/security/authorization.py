from flask_restplus import abort

from app.services.user_service import get_current_user


def check_for_ownership(user_id):
    if get_current_user().id != user_id:
        abort(403, 'You are not allowed to access the resource')


def check_for_idea_ownership(idea):
    if get_current_user().id != idea.author.id:
        abort(403, 'You are not allowed to access the resource')


def check_for_vote_ownership(vote):
    if get_current_user().id != vote.user_id:
        abort(403, 'You are not allowed to access the resource')
