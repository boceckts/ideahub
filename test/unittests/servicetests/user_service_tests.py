import unittest

from app.models import User
from app.services.user_service import get_user_by_id, get_all_users, get_user_by_username, username_exists, \
    email_exists, delete_user_by_id, save_user
from test.base_test_case import BaseTestCase


class UserServiceTest(BaseTestCase):

    def test_get_all_users_empty(self):
        self.assertCountEqual([], get_all_users())

    def test_get_all_users(self):
        user = User()
        user.username = 'testy'
        user.email = 'testy@mail.com'
        self.addModel(user)
        self.addTestModels()
        self.assertCountEqual([user, self.testUser], get_all_users())

    def test_get_user_by_id(self):
        self.addTestModels()
        self.assertEqual(self.testUser, get_user_by_id(self.testUser.id))
        self.assertIsNone(get_user_by_id(1234))

    def test_get_user_by_username(self):
        self.addTestModels()
        self.assertEqual(self.testUser, get_user_by_username(self.testUser.username))
        self.assertIsNone(get_user_by_username('SomeUsername'))

    def test_email_exists(self):
        self.addTestModels()
        self.assertTrue(email_exists(self.testUser.email))
        self.assertFalse(email_exists('some@mail.com'))

    def test_username_exists(self):
        self.addTestModels()
        self.assertTrue(username_exists(self.testUser.username))
        self.assertFalse(username_exists('SomeUsername'))

    def test_delete_user_by_id(self):
        self.addTestModels()
        delete_user_by_id(self.testUser.id)
        self.assertCountEqual([], User.query.all())

    def test_save_user(self):
        save_user(self.testUser)
        self.assertEqual([self.testUser], User.query.all())


if __name__ == '__main__':
    unittest.main()
