import unittest

from app.models.event import Event
from test.base_test_case import BaseTestCase


class EventModelTest(BaseTestCase):

    def test_create_and_save_event(self):
        self.addTestModels()
        self.assertIs(self.testEvent, Event.query.get(self.testEvent.id))


if __name__ == '__main__':
    unittest.main()
