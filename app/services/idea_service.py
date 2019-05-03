from datetime import datetime

from sqlalchemy import func

from app import db
from app.models import Idea, Vote
from app.services.vote_service import delete_votes_for_idea


def get_idea(idea_id):
    return db.session.query(Idea).filter_by(id=idea_id).first()


def idea_exists(idea_id):
    return get_idea(idea_id) is not None


def get_all_ideas():
    return db.session.query(Idea).all()


def get_all_ideas_for_user(user_id):
    return db.session.query(Idea).filter_by(user_id=user_id).order_by(Idea.score.desc()).all()


def get_random_unvoted_idea_for_user(user_id):
    return db.session.query(Idea).filter(~Idea.votes.any(Vote.user_id.is_(user_id))).order_by(func.random()).first()


def idea_title_exists(title):
    return db.session.query(Idea).filter_by(title=title).first() is not None


def edit_idea(idea_id, idea):
    db.session.query(Idea).filter_by(id=idea_id).update({
        Idea.title: idea.title,
        Idea.description: idea.description,
        Idea.tags: idea.tags,
        Idea.categories: idea.categories,
        Idea.modified: datetime.utcnow()
    })
    db.session.commit()


def save_idea(idea):
    db.session.add(idea)
    db.session.commit()


def delete_idea_by_id(idea_id):
    delete_votes_for_idea(idea_id)
    db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
    db.session.commit()


def delete_ideas_for_user(user_id):
    for idea in get_all_ideas_for_user(user_id):
        delete_votes_for_idea(idea.id)
    db.session.query(Idea).filter_by(user_id=user_id).delete(synchronize_session='fetch')
    db.session.commit()
