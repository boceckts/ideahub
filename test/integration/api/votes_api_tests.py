import unittest

from app.models import Vote
from test.integration.base_integration_test_case import IntegrationTestCase


class VotesApiTests(IntegrationTestCase):
    votes_api = '/votes'

    def test_get_votes(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.votes_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testVote.id, json_data[0].get('id'))
            self.assertEqual(self.testVote.value, json_data[0].get('value'))
            self.assertIsNone(json_data[0].get('owner'))
            self.assertIsNone(json_data[0].get('target'))
            self.assertIsNone(json_data[0].get('created'))
            self.assertIsNone(json_data[0].get('modified'))

    def test_post_votes(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.post(self.api_base_path + self.votes_api, json=self.testNewVoteData, headers=headers)
            self.assertEqual(201, response.status_code)
            self.assertIn('/votes/', response.location)

    def test_delete_votes_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.votes_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Vote.query.all())

    def test_get_vote_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.votes_api + '/{}'.format(self.testVote.id), headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testVote.id, json_data.get('id'))
            self.assertEqual(self.testVote.value, json_data.get('value'))
            self.assertEqual(self.testVote.user_id, json_data.get('owner'))
            self.assertEqual(self.testVote.idea_id, json_data.get('target'))
            self.assertIsNotNone(json_data.get('created'))
            self.assertIsNotNone(json_data.get('modified'))

    def test_edit_vote_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.put(self.api_base_path + self.votes_api + '/{}'.format(self.testVote.id),
                             json=self.testEditVoteData,
                             headers=headers)
            self.assertEqual(204, response.status_code)

    def test_delete_vote_by_id(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.votes_api + '/{}'.format(self.testVote.id), headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Vote.query.all())

    def test_delete_vote_by_id_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.votes_api + '/{}'.format(self.testVote.id), headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([], Vote.query.all())


if __name__ == '__main__':
    unittest.main()
