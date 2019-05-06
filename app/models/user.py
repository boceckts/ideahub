import base64
import os
from datetime import datetime, timedelta

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import func, select
from sqlalchemy.orm import column_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.models import Vote, Idea


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tags = db.Column(db.String())
    ideas = db.relationship('Idea', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    votes_count = column_property(
        select([func.count(Vote.id)]).where(Vote.user_id == id)
    )
    idea_count = column_property(
        select([func.count(Idea.id)]).where(Idea.user_id == id)
    )

    def generate_auth_token(self, expires_in=365):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(days=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        user_as_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        user_as_dict['ideas_url'] = url_for('user_ideas_ep', _external=True)
        user_as_dict['votes_url'] = url_for('user_votes_ep', _external=True)
        user_as_dict['ideas_count'] = self.idea_count
        user_as_dict['votes_count'] = self.votes_count
        return user_as_dict


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
