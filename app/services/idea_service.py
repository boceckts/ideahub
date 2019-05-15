from datetime import datetime

from sqlalchemy import func

from app import db
from app.models import Idea, Vote, User
from app.services.event_service import check_idea_change_event, check_idea_delete_event
from app.services.vote_service import delete_votes_for_idea


def get_idea(idea_id):
    return db.session.query(Idea).filter_by(id=idea_id).first()


def get_idea_by_title(title):
    return db.session.query(Idea).filter_by(title=title).first()


def idea_exists(idea_id):
    return get_idea(idea_id) is not None


def get_all_ideas():
    return db.session.query(Idea).order_by(Idea.score.desc()).all()


def get_ideas_by_search(search):
    query = db.session.query(Idea)
    if search.title not in ['any', '']:
        query = query.filter(Idea.title.contains(search.title))
    if search.category not in ['any', '']:
        query = query.filter(Idea.category == search.category)
    if search.tags not in ['any', '']:
        for tag in search.tags.split(','):
            query = query.filter(Idea.tags.contains(tag.strip()))
    query = query.order_by(Idea.score.desc())
    return query.all()


def get_all_ideas_for_user(user_id):
    return db.session.query(Idea).filter_by(user_id=user_id).order_by(Idea.score.desc()).all()


def get_unvoted_ideas_query_for_user(user_id):
    return db.session.query(Idea).filter(~Idea.votes.any(Vote.user_id.is_(user_id)))


def get_random_unvoted_idea_for_user(user_id):
    user = User.query.get(user_id)
    query = get_unvoted_ideas_query_for_user(user_id)
    if user and user.tags is not None:
        for tag in user.tags.split(','):
            query = query.filter(Idea.tags.contains(tag.strip()))
        if query.first() is None:
            query = get_unvoted_ideas_query_for_user(user_id)
    query = query.order_by(func.random())
    return query.first()


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
    return idea


def save_idea_by_json(json_data, user):
    idea = Idea()
    idea.title = json_data['title']
    idea.description = json_data['description']
    idea.category = json_data['category']
    idea.tags = json_data['tags']
    idea.author = user
    return save_idea(idea)


def save_idea_by_form(form, user_id):
    idea = Idea(title=form.title.data,
                description=form.description.data,
                category=form.category.data,
                tags=form.tags.data,
                user_id=user_id)
    return save_idea(idea)


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


def get_top_ten_ideas_by_score():
    return db.session.query(Idea).order_by(Idea.score.desc()).all()[:10]


def get_top_ten_ideas_by_upvotes():
    return db.session.query(Idea).order_by(Idea.upvotes.desc()).all()[:10]


def get_top_ten_ideas_by_downvotes():
    return db.session.query(Idea).order_by(Idea.downvotes.desc()).all()[:10]


def get_top_ten_ideas_by_total_votes():
    return db.session.query(Idea).order_by(Idea.votes_count.desc()).all()[:10]
