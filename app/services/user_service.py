from app import db
from app.models import User
from app.services.idea_service import delete_ideas_for_user
from app.services.vote_service import delete_votes_for_user


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


def delete_user_by_id(user_id):
    delete_votes_for_user(user_id)
    delete_ideas_for_user(user_id)
    db.session.query(User).filter_by(id=user_id).delete(synchronize_session='fetch')
    db.session.commit()


def save_user(user):
    db.session.add(user)
    db.session.commit()


def edit_user_by_json(user_id, json_data):
    db.session.query(User).filter_by(id=user_id).update({
        User.email: json_data['email'],
        User.name: json_data['name'],
        User.surname: json_data['surname'],
    })
    pwd = json_data['password']
    user = get_user_by_id(user_id)
    if pwd is not None and pwd != "":
        user.set_password(pwd)
    db.session.commit()
    return user


def edit_user_by_form(user_id, form_data):
    db.session.query(User).filter_by(id=user_id).update({
        User.name: form_data.name.data,
        User.surname: form_data.surname.data,
    })
    pwd = form_data.password.data
    user = get_user_by_id(user_id)
    if pwd is not None and pwd != "":
        user.set_password(pwd)
    db.session.commit()
    return user
