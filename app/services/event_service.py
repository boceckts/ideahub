from datetime import datetime

from app import db
from app.models import Idea, Vote
from app.models.event import Event, EventType


def get_all_events_for_user(user_id):
    return db.session.query(Event).filter_by(user_id=user_id).order_by(Event.created.desc()).all()


def check_vote_event(vote):
    idea = Idea.query.get(vote.idea_id)
    if vote.value > 0 and idea.upvotes % 5 == 0:
        save_event(Event(type=EventType.upvotes,
                         user_id=idea.user_id,
                         idea_name=idea.title,
                         data=idea.upvotes,
                         created=vote.created))
    elif idea.votes_count % 10 == 0:
        save_event(Event(type=EventType.votes,
                         user_id=idea.user_id,
                         idea_name=idea.title,
                         data=idea.votes_count,
                         created=vote.created))


def check_idea_change_event(idea):
    votes = db.session.query(Vote).filter_by(idea_id=idea.id).filter(Vote.user_id != idea.user_id).all()
    for vote in votes:
        save_event(Event(type=EventType.idea_changed,
                         user_id=vote.user_id,
                         idea_name=idea.title,
                         created=idea.modified))


def check_idea_delete_event(idea):
    votes = db.session.query(Vote).filter_by(idea_id=idea.id).filter(Vote.user_id != idea.user_id).all()
    for vote in votes:
        save_event(Event(type=EventType.idea_deleted,
                         user_id=vote.user_id,
                         idea_name=idea.title,
                         created=datetime.utcnow()))


def save_event(event):
    db.session.add(event)
    db.session.commit()


def delete_events_for_user(user_id):
    db.session.query(Event).filter_by(user_id=user_id).delete(synchronize_session='fetch')
    db.session.commit()
