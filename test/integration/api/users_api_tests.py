import unittest

from app.models import User, Idea, Vote
from app.models.event import Event
from test.integration.base_integration_test_case import IntegrationTestCase


class UsersApiTests(IntegrationTestCase):
    users_api = '/users'

    def test_post_users(self):
        self.addTestModels()
        with self.app as c:
            response = c.post(self.api_base_path + self.users_api, json=self.testNewUserData)
            self.assertEqual(201, response.status_code)
            self.assertIn('/users/', response.location)
            self.assertEqual(self.testUserData, response.get_json())

    def test_get_users(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            response = c.get(self.api_base_path + self.users_api, headers=headers)
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertEqual(self.testUser.id, json_data[1].get('id'))
            self.assertEqual(self.testUser.username, json_data[1].get('username'))
            self.assertIsNotNone(json_data[1].get('ideas_url'))
            self.assertIsNotNone(json_data[1].get('votes_url'))
            self.assertIsNone(json_data[1].get('name'))
            self.assertIsNone(json_data[1].get('surname'))
            self.assertIsNone(json_data[1].get('email'))
            self.assertIsNone(json_data[1].get('tags'))
            self.assertIsNone(json_data[1].get('ideas_count'))
            self.assertIsNone(json_data[1].get('votes_count'))
            self.assertIsNone(json_data[1].get('role'))

    def test_delete_users_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.users_api, headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([self.testAdmin], User.query.all())
            self.assertCountEqual([], Idea.query.all())
            self.assertCountEqual([], Vote.query.all())
            self.assertCountEqual([], Event.query.all())

    def test_delete_user_by_id_as_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.users_api + '/{}'.format(self.testUser.id), headers=headers)
            self.assertEqual(204, response.status_code)
            self.assertCountEqual([self.testAdmin], User.query.all())
            self.assertCountEqual([], Idea.query.all())
            self.assertCountEqual([], Vote.query.all())
            self.assertCountEqual([], Event.query.all())

    def test_delete_admin(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            response = c.delete(self.api_base_path + self.users_api + '/{}'.format(self.testAdmin.id), headers=headers)
            self.assertEqual(403, response.status_code)
            self.assertCountEqual([self.testAdmin, self.testUser], User.query.all())


if __name__ == '__main__':
    unittest.main()
