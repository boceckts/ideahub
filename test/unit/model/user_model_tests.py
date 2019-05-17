import unittest
from datetime import timedelta, datetime

from sqlalchemy.exc import IntegrityError

from app.models import User
from test.base_test_case import BaseTestCase


class UserModelTest(BaseTestCase):

    def test_create_and_save_user(self):
        self.addTestModels()
        self.assertIs(self.testUser, User.query.get(self.testUser.id))

    def test_generate_auth_token(self):
        self.addTestModels()
        self.testUser.revoke_token()
        self.testUser.generate_auth_token(expires_in=1)
        self.assertIsNotNone(self.testUser.token)
        self.assertLess(datetime.utcnow(), self.testUser.token_expiration)
        self.assertGreater(datetime.utcnow() + timedelta(days=1, seconds=1), self.testUser.token_expiration)

    def test_revoke_token(self):
        self.addTestModels()
        self.testUser.generate_auth_token()
        self.assertIsNotNone(self.testUser.token)
        self.testUser.revoke_token()
        self.assertGreater(datetime.utcnow(), self.testUser.token_expiration)

    def test_check_token(self):
        self.addTestModels()
        self.testUser.generate_auth_token()
        self.assertIsNone(User.check_token('abcdefg'))
        self.assertEqual(self.testUser, User.check_token(self.testUser.token))
        self.testUser.revoke_token()
        self.assertIsNone(User.check_token(self.testUser.token))

    def test_set_password(self):
        user = User()
        self.assertIsNone(user.password_hash)
        user.set_password('123456')
        self.assertIsNotNone(user.password_hash)

    def test_check_password(self):
        user = User()
        pwd = 'abc1234'
        user.set_password(pwd)
        self.assertTrue(user.check_password(pwd))
        self.assertFalse(user.check_password(pwd.upper()))

    def test_user_username_constraint(self):
        first_user = User()
        first_user.username = 'MyUserName'
        second_user = User()
        second_user.username = 'MyUserName'
        self.addModel(first_user)
        with self.assertRaises(IntegrityError):
            self.addModel(second_user)

    def test_user_email_constraint(self):
        first_user = User()
        first_user.email = 'name@mail.com'
        second_user = User()
        second_user.email = 'name@mail.com'
        self.addModel(first_user)
        with self.assertRaises(IntegrityError):
            self.addModel(second_user)


if __name__ == '__main__':
    unittest.main()
