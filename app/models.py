from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    ideas = db.relationship('Idea', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='target', lazy='dynamic')

    def __repr__(self):
        return '<Idea %r>' % (self.description)

class Vote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), primary_key=True)
    value = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

    def __repr__(self):
        return '<Vote %r>' % (self.value)