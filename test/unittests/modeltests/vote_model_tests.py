import unittest

from sqlalchemy.exc import IntegrityError

from app.models import Vote
from test.base_test_case import BaseTestCase


class VoteModelTest(BaseTestCase):

    def test_create_and_save_vote(self):
        self.addTestModels()
        self.assertIs(self.testVote, Vote.query.get(self.testVote.id))

    def test_vote_constraints(self):
        first_vote = Vote()
        first_vote.idea_id = 1
        first_vote.user_id = 1
        first_vote.value = 1
        second_vote = Vote()
        second_vote.idea_id = 1
        second_vote.user_id = 1
        second_vote.value = -1
        self.addModel(first_vote)
        with self.assertRaises(IntegrityError):
            self.addModel(second_vote)


if __name__ == '__main__':
    unittest.main()
