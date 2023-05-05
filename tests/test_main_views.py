import datetime

from tests import BasicTestCase
from todo import db
from todo.models import Todo, User


class MainViewsTestCase(BasicTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        super().setUp()
        db.create_all()

        user = User(name='tester', password='tester12')
        db.session.add(user)
        db.session.commit()

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

    def add_todo(self):
        response = self.client.post(
            '/todo/tester',
            data={
                'task_name': 'test',
                'task_content': 'test',
                'task_date': '2022-01-01',
                'task_time': '13:00'
            }
        )
        return response

    def get_user_todos(self):
        response = self.client.get(
            '/todo/tester'
        )
        return response

    def edit_todo(self):
        response = self.client.put(
            '/todo/tester/1',
            data={
                'edit_name': 'edit',
                'edit_content': 'edit',
                'edit_date': '2022-02-02',
                'edit_time': '14:00'
            }
        )
        return response

    def del_todo(self):
        response = self.client.delete(
            '/todo/tester/1'
        )
        return response

    def test_create_todo_valid_return_msg(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.add_todo()
        result = {
            'msg': 'success',
        }
        self.assertDictEqual(response.json, result)
        self.assertIsNotNone(Todo.query.filter_by(task_name='test').first())

    def test_create_todo_invalid_form_return_400(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            '/todo/tester',
            data={
                'task_name': 'test',
                'task_content': '',
                'task_date': '2022/01/01',
                'task_time': '13:00'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(Todo.query.filter_by(task_name='test').first())

    def test_create_todo_not_login_form_return_302(self):
        response = self.add_todo()
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(Todo.query.filter_by(task_name='test').first())

    def test_create_todo_user_not_found_return_404(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            '/todo/fake',
            data={
                'task_name': 'test',
                'task_content': 'test',
                'task_date': '2022-01-01',
                'task_time': '13:00'
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(Todo.query.filter_by(task_name='test').first())

    def test_get_todos_valid_return_msg_and_data(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.get_user_todos()
        result = {
            'msg': 'success',
            'todos': [{
                'task_id': 1,
                'task_name': 'test',
                'task_content': 'test',
                'task_date': '2022-01-01',
                'task_time': '13:00'
            }]
        }
        self.assertDictEqual(response.json, result)

    def test_get_todos_user_not_found_return_404(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            '/todo/fake'
        )
        self.assertEqual(response.status_code, 404)

    def test_get_todos_not_login_return_302(self):
        response = self.get_user_todos()
        self.assertEqual(response.status_code, 302)

    def test_update_todo_valid_return_msg(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.edit_todo()
        result = {
            'msg': 'success',
        }
        self.assertDictEqual(response.json, result)

    def test_update_todo_invalid_form_return_400(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.put(
            '/todo/tester/1',
            data={
                'edit_name': 'abc',
                'edit_content': None,
                'edit_date': '2022/02/02',
                'edit_time': '14:00'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(todo.task_name, 'test')

    def test_update_todo_not_login_return_302(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.edit_todo()
        self.assertEqual(response.status_code, 302)

    def test_update_todo_todo_not_found_return_404(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.put(
            '/todo/tester/2',
            data={
                'edit_name': 'edit',
                'edit_content': 'edit',
                'edit_date': '2022-02-02',
                'edit_time': '14:00'
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(todo.task_name, 'test')

    def test_update_todo_user_not_found_return_404(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.put(
            '/todo/fake/1',
            data={
                'edit_name': 'edit',
                'edit_content': 'edit',
                'edit_date': '2022-02-02',
                'edit_time': '14:00'
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(todo.task_name, 'test')

    def test_update_todo_not_in_user_return_404(self):
        user = User(name='tester2', password='tester12')
        db.session.add(user)
        db.session.commit()

        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        todo_sec = Todo(task_name='test2', task_content='test2',
                        task_date=datetime.date(2022, 1, 1),
                        task_time=datetime.time(13, 0), user_id=2)
        self.assertTrue(todo_sec.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.put(
            '/todo/tester/2',
            data={
                'edit_name': 'edit',
                'edit_content': 'edit',
                'edit_date': '2022-02-02',
                'edit_time': '14:00'
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(todo_sec.task_name, 'test2')

    def test_delete_todo_valid_return_msg(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.del_todo()
        result = {
            'msg': 'success',
        }
        self.assertDictEqual(response.json, result)
        self.assertIsNone(Todo.query.filter_by(task_name='test').first())

    def test_delete_todo_todo_not_found_return_404(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.delete(
            '/todo/tester/2'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Todo.query.filter_by(task_name='test').first())

    def test_delete_todo_user_not_found_return_404(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.delete(
            '/todo/fake/1'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Todo.query.filter_by(task_name='test').first())

    def test_delete_todo_todo_not_in_user_return_404(self):
        user = User(name='tester2', password='tester12')
        db.session.add(user)
        db.session.commit()

        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        todo_sec = Todo(task_name='test2', task_content='test2',
                        task_date=datetime.date(2022, 1, 1),
                        task_time=datetime.time(13, 0), user_id=2)
        self.assertTrue(todo_sec.save())

        response = self.login_user()
        self.assertEqual(response.status_code, 302)

        response = self.client.delete(
            '/todo/tester/2'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Todo.query.filter_by(task_name='test').first())

    def test_delete_todo_not_login_return_302(self):
        todo = Todo(task_name='test', task_content='test',
                    task_date=datetime.date(2022, 1, 1), task_time=datetime.time(13, 0), user_id=1)
        self.assertTrue(todo.save())

        response = self.del_todo()
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Todo.query.filter_by(task_name='test').first())
