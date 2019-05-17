import unittest

from app.models import Idea
from test.integration.base_integration_test_case import IntegrationTestCase


class IdeasApiTests(IntegrationTestCase):
    ideas_api = '/ideas'

    def test_get_ideas(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.ideas_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testIdea.id, json_data[0].get('id'))
            self.assertEqual(self.testIdea.title, json_data[0].get('title'))
            self.assertEqual(self.testIdea.description, json_data[0].get('description'))
            self.assertEqual(self.testIdea.category, json_data[0].get('category'))
            self.assertEqual(self.testIdea.tags, json_data[0].get('tags'))
            self.assertEqual(self.testIdea.score, json_data[0].get('score'))
            self.assertIsNotNone(json_data[0].get('votes_url'))
            self.assertIsNone(json_data[0].get('upvotes'))
            self.assertIsNone(json_data[0].get('downvotes'))
            self.assertIsNone(json_data[0].get('votes_count'))

    def test_post_ideas(self):
        self.addModel(self.testUser)
        self.addModel(self.testIdea)
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.post(self.api_base_path + self.ideas_api, json=self.testNewIdeaData, headers=headers)
            self.assertEqual(201, response.status_code)
            self.assertIn('/ideas/', response.location)

    def test_delete_ideas_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.ideas_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Idea.query.all())

    def test_get_idea_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.ideas_api + '/{}'.format(self.testIdea.id), headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testIdea.id, json_data.get('id'))
            self.assertEqual(self.testIdea.user_id, json_data.get('author'))
            self.assertEqual(self.testIdea.title, json_data.get('title'))
            self.assertEqual(self.testIdea.description, json_data.get('description'))
            self.assertEqual(self.testIdea.category, json_data.get('category'))
            self.assertEqual(self.testIdea.tags, json_data.get('tags'))
            self.assertEqual(self.testIdea.votes_count, json_data.get('votes_count'))
            self.assertEqual(self.testIdea.score, json_data.get('score'))
            self.assertEqual(self.testIdea.upvotes, json_data.get('upvotes'))
            self.assertEqual(self.testIdea.downvotes, json_data.get('downvotes'))
            self.assertIsNotNone(json_data.get('votes_url'))
            self.assertIsNotNone(json_data.get('created'))
            self.assertIsNotNone(json_data.get('modified'))

    def test_edit_idea_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.put(self.api_base_path + self.ideas_api + '/{}'.format(self.testIdea.id),
                             json=self.testEditIdeaData,
                             headers=headers)
            self.assertEqual(204, response.status_code)

    def test_delete_idea_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.ideas_api + '/{}'.format(self.testIdea.id), headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Idea.query.all())

    def test_delete_idea_by_id_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.ideas_api + '/{}'.format(self.testIdea.id), headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Idea.query.all())

    def test_get_idea_votes(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.ideas_api + '/{}'.format(self.testIdea.id) + '/votes',
                             headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testVote.id, json_data[0].get('id'))
            self.assertEqual(self.testVote.value, json_data[0].get('value'))
            self.assertEqual(self.testVote.user_id, json_data[0].get('owner'))
            self.assertEqual(self.testVote.idea_id, json_data[0].get('target'))
            self.assertIsNotNone(json_data[0].get('created'))
            self.assertIsNotNone(json_data[0].get('modified'))


if __name__ == '__main__':
    unittest.main()
