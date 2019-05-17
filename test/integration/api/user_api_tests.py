import unittest

from app.models import User, Vote, Idea
from test.integration.base_integration_test_case import IntegrationTestCase


class UserApiTests(IntegrationTestCase):
    user_api = '/user'
    user_idea_api = '/user/ideas'
    user_votes_api = '/user/votes'

    def test_get_user(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.user_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testUser.id, json_data.get('id'))
            self.assertEqual(self.testUser.name, json_data.get('name'))
            self.assertEqual(self.testUser.surname, json_data.get('surname'))
            self.assertEqual(self.testUser.username, json_data.get('username'))
            self.assertEqual(self.testUser.email, json_data.get('email'))
            self.assertEqual(self.testUser.tags, json_data.get('tags'))
            self.assertEqual(self.testUser.idea_count, json_data.get('ideas_count'))
            self.assertEqual(self.testUser.votes_count, json_data.get('votes_count'))
            self.assertIsNone(json_data.get('role'))
            self.assertIsNotNone(json_data.get('ideas_url'))
            self.assertIsNotNone(json_data.get('votes_url'))

    def test_edit_user_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.put(self.api_base_path + self.user_api,
                             json=self.testEditUserData,
                             headers=headers)
            self.assertEqual(204, response.status_code)

    def test_delete_user(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.user_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([self.testAdmin], User.query.all())

    def test_delete_user_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.user_api, headers=headers)
            self.assertEqual(403, response.status_code)

    def test_get_user_ideas(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.user_idea_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testIdea.id, json_data[0].get('id'))
            self.assertEqual(self.testIdea.user_id, json_data[0].get('author'))
            self.assertEqual(self.testIdea.title, json_data[0].get('title'))
            self.assertEqual(self.testIdea.description, json_data[0].get('description'))
            self.assertEqual(self.testIdea.category, json_data[0].get('category'))
            self.assertEqual(self.testIdea.tags, json_data[0].get('tags'))
            self.assertEqual(self.testIdea.votes_count, json_data[0].get('votes_count'))
            self.assertEqual(self.testIdea.score, json_data[0].get('score'))
            self.assertEqual(self.testIdea.upvotes, json_data[0].get('upvotes'))
            self.assertEqual(self.testIdea.downvotes, json_data[0].get('downvotes'))
            self.assertIsNotNone(json_data[0].get('votes_url'))
            self.assertIsNotNone(json_data[0].get('created'))
            self.assertIsNotNone(json_data[0].get('modified'))

    def test_delete_user_ideas(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.user_idea_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Idea.query.all())

    def test_get_user_votes(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.user_votes_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testVote.id, json_data[0].get('id'))
            self.assertEqual(self.testVote.value, json_data[0].get('value'))
            self.assertEqual(self.testVote.user_id, json_data[0].get('owner'))
            self.assertEqual(self.testVote.idea_id, json_data[0].get('target'))
            self.assertIsNotNone(json_data[0].get('created'))
            self.assertIsNotNone(json_data[0].get('modified'))

    def test_delete_user_votes(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.user_votes_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Vote.query.all())


if __name__ == '__main__':
    unittest.main()
