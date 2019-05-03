from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import column_property

from app import db
from app.models import Vote


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    picture = db.Column(db.BLOB)
    attachments = db.Column(db.BLOB)
    categories = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='target', lazy='dynamic', cascade="all, delete-orphan")
    votes_count = column_property(
        select([func.count(Vote.id)]).where(Vote.idea_id == id)
    )
    upvotes = column_property(
        select([func.count(Vote.value)]).where(Vote.idea_id == id).where(Vote.value == 1)
    )
    downvotes = column_property(
        select([func.count(Vote.value)]).where(Vote.idea_id == id).where(Vote.value == -1)
    )
    score = column_property(
        select([func.sum(Vote.value)]).where(Vote.idea_id == id)
    )

    def __repr__(self):
        return '<Idea %r>' % self.title

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
