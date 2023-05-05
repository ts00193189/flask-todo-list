from tests import BasicTestCase
from todo import db


class AuthViewsTestCase(BasicTestCase):
    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()

    def login_user(self):
        response = self.client.post(
            '/auth/login',
            data={
                'user_name': 'tester',
                'password': 'tester12'
            }
        )
        return response

    def register_user(self):
        response = self.client.post(
            '/auth/register',
            data={
                'user_name': 'tester',
                'password': 'tester12',
                'confirm_password': 'tester12'
            }
        )
        return response

    def test_register_valid_return_302(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 302)

    def test_register_repeat_user_return_invalid_message(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 302)
        response = self.register_user()
        self.assertIn('User name already exist.',
                      response.get_data(as_text=True))

    def test_login_exist_user_return_302(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 302)
        response = self.login_user()
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_form_return_invalid_message(self):
        response = self.client.post('/auth/login', data={})
        self.assertIn('This field is required.',
                      response.get_data(as_text=True))

    def test_login_user_not_found_return_invalid_message(self):
        response = self.login_user()
        self.assertIn('Invalid username or password',
                      response.get_data(as_text=True))

    def test_logout_return_302(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 302)
        response = self.login_user()
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 302)
