import unittest

from app.models import Vote
from test.base_test_case import BaseTestCase


class VoteModelTest(BaseTestCase):

    def test_create_and_save_vote(self):
        self.addTestModels()
        self.assertIs(self.testVote, Vote.query.get(self.testVote.id))


if __name__ == '__main__':
    unittest.main()
