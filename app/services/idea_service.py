from datetime import datetime

from sqlalchemy import func

from app import db
from app.models import Idea, Vote
from app.services.event_service import check_idea_change_event, check_idea_delete_event
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


def edit_idea_by_json(idea_id, json_data):
    db.session.query(Idea).filter_by(id=idea_id).update({
        Idea.title: json_data['title'],
        Idea.description: json_data['description'],
        Idea.category: json_data['category'],
        Idea.tags: json_data['tags'],
        Idea.modified: datetime.utcnow()
    })
    db.session.commit()
    idea = get_idea(idea_id)
    check_idea_change_event(idea)
    return idea


def edit_idea_by_form(idea_id, form_data):
    db.session.query(Idea).filter_by(id=idea_id).update({
        Idea.description: form_data.description.data,
        Idea.tags: form_data.tags.data,
        Idea.category: form_data.category.data,
        Idea.modified: datetime.utcnow()
    })
    db.session.commit()
    idea = get_idea(idea_id)
    check_idea_change_event(idea)
    return idea


def save_idea(idea):
    db.session.add(idea)
    db.session.commit()


def delete_idea_by_id(idea_id):
    check_idea_delete_event(get_idea(idea_id))
    delete_votes_for_idea(idea_id)
    db.session.query(Idea).filter_by(id=idea_id).delete(synchronize_session='fetch')
    db.session.commit()


def delete_ideas_for_user(user_id):
    for idea in get_all_ideas_for_user(user_id):
        check_idea_delete_event(idea)
        delete_votes_for_idea(idea.id)
    db.session.query(Idea).filter_by(user_id=user_id).delete(synchronize_session='fetch')
    db.session.commit()
