import unittest

from app.models import Idea
from test.base_test_case import BaseTestCase


class IdeaModelTest(BaseTestCase):

    def test_create_and_save_idea(self):
        self.addTestModels()
        self.assertIs(self.testIdea, Idea.query.get(self.testIdea.id))


if __name__ == '__main__':
    unittest.main()
