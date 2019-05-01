from app import db
from app.models import Vote


def vote_exists(user_id, idea_id):
    existing_vote = Vote.query.filter_by(user_id=user_id, idea_id=idea_id).first()
    if existing_vote is None:
        return False
    return True


def save_vote(vote):
    db.session.add(vote)
    db.session.commit()
