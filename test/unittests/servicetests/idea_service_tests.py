import random
import unittest
from random import randint

from app.models import Idea, User, Vote
from app.models.search import Search
from app.services.idea_service import get_all_ideas, get_idea, get_idea_by_title, idea_exists, idea_title_exists, \
    delete_idea_by_id, save_idea, get_ideas_by_search, get_all_ideas_for_user, get_unvoted_ideas_query_for_user, \
    get_random_unvoted_idea_for_user, delete_ideas_for_user, get_top_ten_ideas_by_score, get_top_ten_ideas_by_upvotes, \
    get_top_ten_ideas_by_total_votes, get_top_ten_ideas_by_downvotes
from test.base_test_case import BaseTestCase


class IdeaServiceTest(BaseTestCase):

    def test_get_idea(self):
        self.addTestModels()
        self.assertEqual(self.testIdea, get_idea(self.testIdea.id))
        self.assertIsNone(get_idea(1234))

    def test_get_idea_by_title(self):
        self.addTestModels()
        self.assertEqual(self.testIdea, get_idea_by_title(self.testIdea.title))
        self.assertIsNone(get_idea_by_title('Some Idea Title'))

    def test_idea_exists(self):
        self.addTestModels()
        self.assertTrue(idea_exists(self.testIdea.id))
        self.assertFalse(idea_exists(1234))

    def test_get_all_ideas_empty(self):
        self.assertCountEqual([], get_all_ideas())

    def test_get_all_ideas(self):
        self.addTestModels()
        idea = Idea()
        idea.title = 'Testy Title'
        idea.description = 'Testy Description'
        idea.user_id = self.testUser.id
        self.addModel(idea)
        self.assertCountEqual([idea, self.testIdea], get_all_ideas())

    def test_get_ideas_by_search(self):
        self.addTestModels()
        idea = Idea()
        idea.title = 'Unique Title'
        idea.category = 'Unique Category'
        idea.tags = 'Unique Tag'
        idea.user_id = self.testUser.id
        self.addModel(idea)
        search = Search()
        self.assertCountEqual([self.testIdea, idea], get_ideas_by_search(search))
        search.title = 'Unique'
        self.assertEqual([idea], get_ideas_by_search(search))
        search.category = 'Unique Category'
        self.assertEqual([idea], get_ideas_by_search(search))
        search.tags = 'Unique'
        self.assertEqual([idea], get_ideas_by_search(search))

    def test_get_all_ideas_for_user(self):
        self.addTestModels()
        self.assertEqual([self.testIdea], get_all_ideas_for_user(self.testUser.id))

    def test_get_unvoted_ideas_query_for_user(self):
        self.addTestModels()
        self.assertEqual([], get_unvoted_ideas_query_for_user(self.testUser.id).all())
        user = User()
        user.username = 'NewUser'
        user.email = 'newuser@mail.com'
        self.addModel(user)
        self.assertEqual([self.testIdea], get_unvoted_ideas_query_for_user(user.id).all())

    def test_get_random_unvoted_idea_for_user(self):
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        idea = Idea()
        idea.title = 'Unique Title'
        idea.category = 'Unique Category'
        idea.tags = 'Unique Tag'
        self.addModel(idea)
        self.assertEqual(self.testIdea, get_random_unvoted_idea_for_user(self.testUser.id))

    def test_idea_title_exists(self):
        self.addTestModels()
        self.assertTrue(idea_title_exists(self.testIdea.title))
        self.assertFalse(idea_title_exists('Some Idea Title'))

    def test_save_idea(self):
        save_idea(self.testIdea)
        self.assertEqual([self.testIdea], Idea.query.all())

    def test_delete_idea_by_id(self):
        self.addTestModels()
        delete_idea_by_id(self.testIdea.id)
        self.assertCountEqual([], Idea.query.all())

    def test_delete_ideas_for_user(self):
        self.addTestModels()
        delete_ideas_for_user(self.testUser.id)
        self.assertListEqual([], self.testUser.ideas.all())
        self.assertEqual(0, self.testUser.idea_count)
        self.assertListEqual([], Idea.query.all())

    def test_get_top_ten_ideas_by_score(self):
        ideas = self.addIdeas()
        self.addVotes(ideas)
        top_ten = get_top_ten_ideas_by_score()
        self.assertEqual(10, len(top_ten))
        top = Idea.query.order_by(Idea.score.desc()).first()
        self.assertEqual(top, top_ten[0])

    def test_get_top_ten_ideas_by_upvotes(self):
        ideas = self.addIdeas()
        self.addVotes(ideas)
        top_ten = get_top_ten_ideas_by_upvotes()
        self.assertEqual(10, len(top_ten))
        top = Idea.query.order_by(Idea.upvotes.desc()).first()
        self.assertEqual(top, top_ten[0])

    def test_get_top_ten_ideas_by_downvotes(self):
        ideas = self.addIdeas()
        self.addVotes(ideas)
        top_ten = get_top_ten_ideas_by_downvotes()
        self.assertEqual(10, len(top_ten))
        top = Idea.query.order_by(Idea.downvotes.desc()).first()
        self.assertEqual(top, top_ten[0])

    def test_get_top_ten_ideas_by_total_votes(self):
        ideas = self.addIdeas()
        self.addVotes(ideas)
        top_ten = get_top_ten_ideas_by_total_votes()
        self.assertEqual(10, len(top_ten))
        top = Idea.query.order_by(Idea.votes_count.desc()).first()
        self.assertEqual(top, top_ten[0])

    def addIdeas(self):
        ideas = []
        for i in range(15):
            idea = Idea()
            idea.title = str(i)
            self.addModel(idea)
            ideas.append(idea)
        return ideas

    def addVotes(self, ideas):
        votes = []
        for i in range(20):
            vote = Vote()
            vote.value = random.choice([-1, 1])
            vote.idea_id = ideas[randint(0, 14)].id
            self.addModel(vote)
            votes.append(vote)
        return votes


if __name__ == '__main__':
    unittest.main()
