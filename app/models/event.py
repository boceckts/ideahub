import enum
from datetime import datetime

from app import db


class EventType(enum.Enum):
    votes = 1
    upvotes = 2
    idea_changed = 3
    idea_deleted = 4


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.Enum(EventType))
    idea_name = db.Column(db.String)
    data = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Event %r>' % self.type

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
