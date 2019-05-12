import unittest

from sqlalchemy.exc import IntegrityError

from app.models import Idea
from test.base_test_case import BaseTestCase


class IdeaModelTest(BaseTestCase):

    def test_create_and_save_idea(self):
        self.addTestModels()
        self.assertIs(self.testIdea, Idea.query.get(self.testIdea.id))

    def test_idea_title_constraint(self):
        first_idea = Idea()
        first_idea.title = 'MyTitle'
        second_idea = Idea()
        second_idea.title = 'MyTitle'
        self.addModel(first_idea)
        with self.assertRaises(IntegrityError):
            self.addModel(second_idea)


if __name__ == '__main__':
    unittest.main()
