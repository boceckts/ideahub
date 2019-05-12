import unittest

from app.models import User, Vote
from app.models.event import Event, EventType
from app.services.event_service import save_event, get_all_events_for_user, delete_events_for_user, \
    check_idea_change_event, check_idea_delete_event, check_vote_event
from test.base_test_case import BaseTestCase


class EventServiceTest(BaseTestCase):

    def test_get_all_events_for_user_empty(self):
        self.addModel(self.testUser)
        self.assertCountEqual([], get_all_events_for_user(self.testUser.id))

    def test_get_all_events_for_user(self):
        self.addTestModels()
        event = Event()
        event.user_id = self.testUser.id
        self.addModel(event)
        self.assertCountEqual([event, self.testEvent], get_all_events_for_user(self.testUser.id))

    def test_check_vote_event(self):
        self.addModel(self.testUser)
        self.testIdea.user_id = self.testUser.id
        self.addModel(self.testIdea)
        for i in range(10):
            user = User()
            user.username = str(i)
            user.email = '{}@mail.com'.format(i)
            self.addModel(user)
            vote = Vote()
            vote.idea_id = self.testIdea.id
            vote.user_id = user.id
            vote.value = 1
            self.addModel(vote)
            check_vote_event(vote)
            if i == 5:
                self.assertEqual(EventType.upvotes, Event.query.first().type)
            elif i == 10:
                self.assertEqual(EventType.votes, Event.query.first().type)

    def test_check_idea_change_event(self):
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        self.testVote.idea_id = self.testIdea.id
        self.testVote.user_id = self.testUser.id
        self.addModel(self.testVote)
        check_idea_change_event(self.testIdea)
        self.assertEqual(EventType.idea_changed, Event.query.first().type)

    def test_check_idea_delete_event(self):
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        self.testVote.idea_id = self.testIdea.id
        self.testVote.user_id = self.testUser.id
        self.addModel(self.testVote)
        check_idea_delete_event(self.testIdea)
        self.assertEqual(EventType.idea_deleted, Event.query.first().type)

    def test_save_event(self):
        self.addModel(self.testUser)
        self.testEvent.user_id = self.testUser.id
        save_event(self.testEvent)
        self.assertEqual([self.testEvent], Event.query.all())

    def test_delete_events_for_user(self):
        self.addTestModels()
        delete_events_for_user(self.testUser.id)
        self.assertCountEqual([], Event.query.all())


if __name__ == '__main__':
    unittest.main()
