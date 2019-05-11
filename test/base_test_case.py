import os
import unittest

from app import app, db
from app.models import User, Idea, Vote
from app.models.event import Event, EventType


class BaseTestCase(unittest.TestCase):
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
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        self.addModel(self.testVote)
        self.addModel(self.testEvent)

    def setTestUser(self):
        self.testUser = User()
        self.testUser.username = 'john'
        self.testUser.name = 'John'
        self.testUser.surname = 'Doe'
        self.testUser.email = 'john@mail.com'
        self.testUser.tags = 'web development, csse'
        self.testUser.set_password('123456')

    def setTestIdea(self):
        self.testIdea = Idea()
        self.testIdea.title = 'My Awesome Test Idea'
        self.testIdea.description = 'Description of an Awesome Test Idea'
        self.testIdea.category = 'Engineering'
        self.testIdea.tags = self.testUser.tags
        self.testIdea.user_id = self.testUser.id

    def setTestVote(self):
        self.testVote = Vote()
        self.testVote.value = 1
        self.testVote.idea_id = self.testIdea.id
        self.testVote.user_id = self.testUser.id

    def setTestEvent(self):
        self.testEvent = Event()
        self.testEvent.type = EventType.votes
        self.testEvent.user_id = self.testUser.id
        self.testEvent.idea_name = self.testIdea.title
        self.testEvent.data = 10
