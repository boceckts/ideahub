from flask import g

from app import db
from app.models import User
from app.services.idea_service import delete_ideas_for_user
from app.services.vote_service import delete_votes_for_user


def get_current_user():
    return g.current_user


def set_current_user(user):
    g.current_user = user


def get_all_users():
    return db.session.query(User).all()


def get_user_by_id(user_id):
    return db.session.query(User).filter_by(id=user_id).first()


def get_user_by_username(username):
    return db.session.query(User).filter_by(username=username).first()


def email_exists(email):
    return db.session.query(User).filter_by(email=email).first() is not None


def username_exists(username):
    return db.session.query(User).filter_by(username=username).first() is not None


def delete_current_user():
    user_id = get_current_user().id
    delete_votes_for_user(user_id)
    delete_ideas_for_user(user_id)
    db.session.query(User).filter_by(id=get_current_user().id).delete(synchronize_session='fetch')
    db.session.commit()


def save_user(user):
    db.session.add(user)
    db.session.commit()


def save_new_user(user):
    db.session.add(user)
    db.session.commit()


def edit_current_user(json_data):
    db.session.query(User).filter_by(id=get_current_user().id).update({
        User.email: json_data['email'],
        User.name: json_data['name'],
        User.surname: json_data['surname'],
    })
    get_current_user().set_password(json_data['password'])
    db.session.commit()
    return get_current_user()


def edit_current_user_by_for(form_data):
    db.session.query(User).filter_by(id=get_current_user().id).update({
        User.email: form_data.email.data,
        User.name: form_data.name.data,
        User.surname: form_data.surname.data,
    })
    db.session.commit()
    return get_current_user()
