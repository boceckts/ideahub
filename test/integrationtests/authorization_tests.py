import unittest

from test.integrationtests.base_integration_test_case import IntegrationBaseTestCase


class AuthorizationTests(IntegrationBaseTestCase):

    def test_unauthenticated_access_to_resources(self):
        base_resources = ['/users', '/ideas', '/votes', '/token']
        with self.app as c:
            for r in base_resources:
                if not r == '/token':
                    response = c.get(self.api_base_path + r)
                    self.assertEqual(401, response.status_code, 'show resource {} not secured'.format(r))
                if r == '/ideas':
                    response = c.put(self.api_base_path + r + '/1', json=self.editTestIdea)
                    self.assertEqual(401, response.status_code, 'update resource {} not secured'.format(r))
                elif r == '/votes':
                    response = c.put(self.api_base_path + r + '/1', json=self.editTestVote)
                    self.assertEqual(401, response.status_code, 'update resource {} not secured'.format(r))
                if r == '/ideas':
                    response = c.post(self.api_base_path + r, json=self.newTestIdea)
                    self.assertEqual(401, response.status_code, 'create resource {} not secured'.format(r))
                elif r == '/votes':
                    response = c.post(self.api_base_path + r, json=self.newTestVote)
                    self.assertEqual(401, response.status_code, 'create resource {} not secured'.format(r))
                elif not r == '/users':
                    response = c.post(self.api_base_path + r)
                    self.assertEqual(401, response.status_code, 'create resource {} not secured'.format(r))
                response = c.delete(self.api_base_path + r)
                self.assertEqual(401, response.status_code, 'delete resource {} not secured'.format(r))

    def test_authenticated_access_to_resources(self):
        self.addTestModels()
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        base_resources = ['/users', '/ideas', '/votes', '/token']
        with self.app as c:
            for r in base_resources:
                if not r == '/token':
                    response = c.get(self.api_base_path + r, headers=headers)
                    self.assertEqual(200, response.status_code, 'not allowed to show resource {}'.format(r))
                if r == '/ideas':
                    response = c.post(self.api_base_path + r, json=self.newTestIdea, headers=headers)
                    self.assertEqual(201, response.status_code, 'not allowed to create resource {}'.format(r))
                elif r == '/votes':
                    response = c.post(self.api_base_path + r, json=self.newTestVote, headers=headers)
                    self.assertEqual(201, response.status_code, 'not allowed to create resource {}'.format(r))
                if r == '/ideas':
                    response = c.put(self.api_base_path + r + '/1', json=self.editTestIdea, headers=headers)
                    self.assertEqual(204, response.status_code, 'not allowed to update resource {}'.format(r))
                elif r == '/votes':
                    response = c.put(self.api_base_path + r + '/1', json=self.editTestVote, headers=headers)
                    self.assertEqual(204, response.status_code, 'not allowed to update resource {}'.format(r))

    def test_unauthorized_access_to_admin_resource(self):
        self.addTestModels()
        admin_resources = ['/users/{}'.format(self.testUser.id), '/users', '/ideas', '/votes']
        headers = {'Authorization': 'Bearer {}'.format(self.testUser.token)}
        with self.app as c:
            for r in admin_resources:
                response = c.delete(self.api_base_path + r, headers=headers)
                self.assertEqual(403, response.status_code, 'delete resource {} not secured'.format(r))

    def test_authorized_access_to_admin_resources(self):
        self.addTestModels()
        admin_resources = ['/users/{}'.format(self.testUser.id), '/users', '/ideas', '/votes']
        headers = {'Authorization': 'Bearer {}'.format(self.testAdmin.token)}
        with self.app as c:
            for r in admin_resources:
                response = c.delete(self.api_base_path + r, headers=headers)
                self.assertEqual(204, response.status_code, 'not allowed to delete resource {}'.format(r))


if __name__ == '__main__':
    unittest.main()
