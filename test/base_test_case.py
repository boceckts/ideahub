import os
import unittest

from app import app, db
from app.models import User, Idea, Vote
from app.models.event import Event, EventType
from app.models.user import UserRole


class BaseTestCase(unittest.TestCase):
    testAdmin = None
    testUser = None
    testIdea = None
    testVote = None
    testEvent = None

    def setUp(self):
        self.db = db
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        self.db.create_all()
        self.setTestAdmin()
        self.setTestUser()
        self.setTestIdea()
        self.setTestVote()
        self.setTestEvent()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def addModel(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def addTestModels(self):
        self.addModel(self.testAdmin)
        self.addModel(self.testUser)
        self.testIdea.user_id = self.testUser.id
        self.addModel(self.testIdea)
        self.testVote.idea_id = self.testIdea.id
        self.testVote.user_id = self.testUser.id
        self.addModel(self.testVote)
        self.testEvent.user_id = self.testUser.id
        self.addModel(self.testEvent)

    def setTestAdmin(self):
        self.testAdmin = User()
        self.testAdmin.username = 'admin'
        self.testAdmin.email = 'admin@ideahub.com'
        self.testAdmin.role = UserRole.admin
        self.testAdmin.set_password('123456')
        self.testAdmin.generate_auth_token()

    def setTestUser(self):
        self.testUser = User()
        self.testUser.username = 'john'
        self.testUser.name = 'John'
        self.testUser.surname = 'Doe'
        self.testUser.email = 'john@mail.com'
        self.testUser.tags = 'web development, csse'
        self.testUser.set_password('123456')
        self.testUser.generate_auth_token()

    def setTestIdea(self):
        self.testIdea = Idea()
        self.testIdea.title = 'My Awesome Test Idea'
        self.testIdea.description = 'Description of an Awesome Test Idea'
        self.testIdea.category = 'Engineering'
        self.testIdea.tags = self.testUser.tags

    def setTestVote(self):
        self.testVote = Vote()
        self.testVote.value = 1

    def setTestEvent(self):
        self.testEvent = Event()
        self.testEvent.type = EventType.votes
        self.testEvent.idea_name = self.testIdea.title
        self.testEvent.data = 10
