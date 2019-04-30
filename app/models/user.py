from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ideas = db.relationship('Idea', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
