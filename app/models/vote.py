from datetime import datetime

from sqlalchemy import UniqueConstraint

from app import db


class Vote(db.Model):
    __table_args__ = (UniqueConstraint('user_id', 'idea_id', name='unique_user_idea'),)
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))
    value = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Vote %r>' % self.value

    def as_dict(self):
        vote_as_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        vote_as_dict['target'] = self.idea_id
        vote_as_dict['owner'] = self.user_id
        return vote_as_dict
