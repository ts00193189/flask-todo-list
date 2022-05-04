import unittest
from todo.models import User


class UserModelTestCase(unittest.TestCase):

    def test_password_setter_hash_not_none_return_true(self):
        user = User(password='test')
        self.assertIsNotNone(user.password_hash)

    def test_password_setter_set_same_password_but_not_equal_return_true(self):
        user_first = User(password='test1')
        user_second = User(password='test1')
        self.assertNotEqual(user_first.password_hash, user_second.password_hash)

    def test_password_getter_raise_exception(self):
        user = User(password='test')
        with self.assertRaises(AttributeError):
            user.password

    def test_verify_password_correct_return_true(self):
        user = User(password='test')
        self.assertTrue(user.verify_password('test'))

    def test_verify_password_incorrect_return_false(self):
        user = User(password='test')
        self.assertFalse(user.verify_password('123'))
