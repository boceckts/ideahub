from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ideas = db.relationship('Idea', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    picture = db.Column(db.BLOB)
    attachments = db.Column(db.BLOB)
    categories = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='target', lazy='dynamic')

    def __repr__(self):
        return '<Idea %r>' % self.title


class Vote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), primary_key=True)
    value = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

    def __repr__(self):
        return '<Vote %r>' % self.value

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
