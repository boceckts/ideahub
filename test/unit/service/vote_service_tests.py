import unittest

from app.models import Vote, User
from app.services.vote_service import vote_exists, get_vote, get_vote_by_id, get_all_votes, edit_vote, save_vote, \
    delete_vote_by_id, delete_votes_for_user, delete_votes_for_idea
from test.base_test_case import BaseTestCase


class VoteServiceTest(BaseTestCase):

    def test_vote_exists(self):
        self.addTestModels()
        self.assertTrue(vote_exists(self.testUser.id, self.testIdea.id))
        self.assertFalse(vote_exists(1234, 1234))

    def test_get_vote(self):
        self.addTestModels()
        self.assertEqual(self.testVote, get_vote(self.testUser.id, self.testIdea.id))
        self.assertIsNone(get_vote(1234, 1234))

    def test_get_vote_by_id(self):
        self.addTestModels()
        self.assertEqual(self.testVote, get_vote_by_id(self.testVote.id))
        self.assertIsNone(get_vote_by_id(1234))

    def test_get_all_votes_empty(self):
        self.assertCountEqual([], get_all_votes())

    def test_get_all_votes(self):
        self.addTestModels()
        user = User()
        user.username = 'NewUSer'
        user.email = 'newuser@mail.com'
        self.addModel(user)
        vote = Vote()
        vote.value = 1
        vote.user_id = user.id
        vote.email = self.testIdea.id
        self.addModel(vote)
        self.assertCountEqual([vote, self.testVote], get_all_votes())

    def test_edit_vote(self):
        self.addTestModels()
        edit_vote(self.testVote.id, -1)
        self.assertNotEqual(self.testVote.value, get_vote_by_id(self.testVote.id))

    def test_save_vote(self):
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        self.testVote.idea_id = self.testIdea.id
        self.testVote.user_id = self.testUser.id
        save_vote(self.testVote)
        self.assertEqual([self.testVote], Vote.query.all())

    def test_delete_vote_by_id(self):
        self.addTestModels()
        delete_vote_by_id(self.testVote.id)
        self.assertCountEqual([], Vote.query.all())

    def test_delete_votes_for_user(self):
        self.addTestModels()
        delete_votes_for_user(self.testUser.id)
        self.assertCountEqual([], self.testUser.votes)
        self.assertEqual(0, self.testUser.votes_count)

    def test_delete_votes_for_idea(self):
        self.addTestModels()
        delete_votes_for_idea(self.testIdea.id)
        self.assertCountEqual([], self.testIdea.votes)
        self.assertEqual(0, self.testIdea.votes_count)


if __name__ == '__main__':
    unittest.main()
