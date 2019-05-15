from datetime import datetime

from app import db
from app.models import Vote
from app.services.event_service import check_vote_event


def vote_exists(user_id, idea_id):
    return get_vote(user_id, idea_id) is not None


def get_vote(user_id, idea_id):
    return db.session.query(Vote).filter_by(user_id=user_id, idea_id=idea_id).first()


def get_votes(idea_id):
    return db.session.query(Vote).filter_by(idea_id=idea_id).order_by(Vote.modified.desc()).all()


def get_vote_by_id(vote_id):
    return db.session.query(Vote).filter_by(id=vote_id).first()


def get_all_votes():
    return db.session.query(Vote).all()


def edit_vote(vote_id, value):
    db.session.query(Vote).filter_by(id=vote_id).update({
        Vote.value: value,
        Vote.modified: datetime.utcnow()
    })
    db.session.commit()


def save_vote(vote):
    db.session.add(vote)
    db.session.commit()
    check_vote_event(vote)


def delete_vote_by_id(vote_id):
    db.session.query(Vote).filter_by(id=vote_id).delete(synchronize_session='fetch')
    db.session.commit()


def delete_votes_for_user(user_id):
    db.session.query(Vote).filter_by(user_id=user_id).delete(synchronize_session='fetch')
    db.session.commit()


def delete_votes_for_idea(idea_id):
    db.session.query(Vote).filter_by(idea_id=idea_id).delete(synchronize_session='fetch')
    db.session.commit()
