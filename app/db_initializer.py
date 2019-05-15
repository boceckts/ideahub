import random

from app import app, db
from app.models import User, Idea, Vote
from app.models.event import EventType, Event
from app.models.user import UserRole

PWD = '123456'


@app.cli.command('create-admin')
def create_admin():
    existing_admin = User.query.filter(User.username == 'admin').first()
    if existing_admin is not None:
        print('Admin user already present, will override.')
        User.query.filter(User.username == 'admin').delete()
        db.session.commit()
    admin = User()
    admin.username = 'admin'
    admin.email = 'admin@ideahub.com'
    admin.role = UserRole.admin
    admin.set_password(app.config['ADMIN_PWD'])
    db.session.add(admin)
    db.session.commit()
    print('Admin created with password ' + app.config['ADMIN_PWD'])


@app.cli.command('init-db')
def init_db():
    if db.session.query(User).filter(User.username == 'initial1').first() is not None:
        print('database initialization canceled, database is already initialized.')
    else:
        init_users()
        init_votes()


def init_users():
    print('creating {} users and ideas.'.format(len(users)))
    for name in users:
        user = User()
        user.username = '{}1'.format(name.lower())
        user.name = name
        user.surname = 'Doe'
        user.email = '{}@mail.com'.format(name)
        user.tags = '{},tag-{},#{}'.format(name.lower(), name.lower(), name.lower())
        user.set_password(PWD)
        db.session.add(user)
        db.session.commit()
        add_idea(user)


def add_idea(user):
    idea = Idea()
    idea.title = '{} Awesome Idea'.format(user.username)
    idea.description = 'Description of an awesome Idea of {} with the title {}'.format(user.username, idea.title)
    idea.category = 'Engineering'
    idea.tags = '{},tag-{},#{},{}'.format(user.name.lower(), user.name.lower(), user.name.lower(), idea.title)
    idea.user_id = user.id
    db.session.add(idea)
    db.session.commit()


def init_votes():
    queried_users = db.session.query(User).filter(User.name.in_(users)).all()
    queried_ideas = db.session.query(Idea).all()
    print('creating votes and events for users.')
    for user in queried_users:
        for idea in queried_ideas:
            if random.choice([True, False]):
                vote = Vote()
                vote.value = random.choice([-1, 1])
                vote.idea_id = idea.id
                vote.user_id = user.id
                db.session.add(vote)
                db.session.commit()
                init_event(vote)


def init_event(vote):
    idea = Idea.query.get(vote.idea_id)
    if vote.value > 0 and idea.upvotes % 5 == 0:
        event = (Event(type=EventType.upvotes,
                       user_id=idea.user_id,
                       idea_name=idea.title,
                       data=idea.upvotes,
                       created=vote.created))
        db.session.add(event)
        db.session.commit()
    elif idea.votes_count % 10 == 0:
        event = (Event(type=EventType.votes,
                       user_id=idea.user_id,
                       idea_name=idea.title,
                       data=idea.votes_count,
                       created=vote.created))
        db.session.add(event)
        db.session.commit()


users = [
    "Initial",
    "Liam",
    "William",
    "James",
    "Logan",
    "Benjamin",
    "Mason",
    "Elijah",
    "Oliver",
    "Jacob",
    "Lucas",
    "Michael",
    "Alexander",
    "Ethan",
    "Daniel",
    "Matthew",
    "Aiden",
    "Henry",
    "Joseph",
    "Jackson",
    "Samuel",
    "Sebastian",
    "David",
    "Carter",
    "Wyatt",
    "Jayden",
    "John",
    "Owen",
    "Dylan",
    "Luke",
    "Gabriel",
    "Anthony",
    "Isaac",
    "Grayson",
    "Jack",
    "Julian",
    "Levi",
    "Christopher",
    "Joshua",
    "Andrew",
    "Lincoln",
    "Mateo",
    "Ryan",
    "Jaxon",
    "Nathan",
    "Aaron",
    "Isaiah",
    "Thomas",
    "Charles",
    "Caleb"
]
