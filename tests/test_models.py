import datetime

from tests import BasicTestCase
from todo import db
from todo.models import Todo, User


class UserModelTestCase(BasicTestCase):
    def test_password_setter_hash_not_none_return_true(self):
        user = User(password='test')
        self.assertIsNotNone(user.password_hash)

    def test_password_setter_set_same_password_but_not_equal_hash_return_true(self):
        user_first = User(password='test1')
        user_second = User(password='test1')
        self.assertNotEqual(user_first.password_hash,
                            user_second.password_hash)

    def test_password_getter_raise_exception(self):
        user = User(password='test')
        with self.assertRaises(AttributeError):
            user.password  # pylint: disable=pointless-statement

    def test_verify_password_correct_return_true(self):
        user = User(password='test')
        self.assertTrue(user.verify_password('test'))

    def test_verify_password_incorrect_return_false(self):
        user = User(password='test')
        self.assertFalse(user.verify_password('123'))


class TodoModelTestCase(BasicTestCase):
    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()

    def register_tester(self):
        user = User(name='tester', password='test')
        db.session.add(user)
        db.session.commit()
        return user

    def test_save_valid_return_same_todo(self):
        user = self.register_tester()
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=user.id)
        self.assertTrue(todo.save())
        self.assertEqual(todo, Todo.query.filter_by(id=todo.id).first())

    def test_save_not_user_not_found_return_Fasle(self):
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=42)
        self.assertFalse(todo.save())
        self.assertFalse(todo.query.filter_by(id=todo.id).first())

    def test_delete_valid_return_None(self):
        user = self.register_tester()
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=user.id)
        self.assertTrue(todo.save())
        self.assertEqual(todo, Todo.query.filter_by(id=todo.id).first())
        self.assertTrue(todo.delete())
        self.assertIsNone(Todo.query.filter_by(id=todo.id).first())

    def test_delete_todo_not_found_return_False(self):
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=42)
        self.assertFalse(todo.delete())

    def test_update_valid_return_updated_todo(self):
        user = self.register_tester()
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=user.id)
        self.assertTrue(todo.save())
        self.assertEqual(todo, Todo.query.filter_by(id=todo.id).first())
        self.assertTrue(todo.update(task_name='update', task_content='update',
                                    task_date=datetime.datetime.now().date(),
                                    task_time=datetime.datetime.now().time()))
        self.assertEqual(Todo.query.filter_by(
            id=todo.id).first().task_name, 'update')

    def test_update_invalid_return_not_equal_todo(self):
        user = self.register_tester()
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=user.id)
        self.assertTrue(todo.save())
        self.assertEqual(todo, Todo.query.filter_by(id=todo.id).first())
        self.assertFalse(todo.update(task_name='update', task_content='update',
                                     task_date='2040-01-01',
                                     task_time='11:11'))
        self.assertNotEqual(Todo.query.filter_by(
            id=todo.id).first().task_name, 'update')

    def test_serialize_return_dict(self):
        todo = Todo(task_name='test', task_content='test', task_date=datetime.datetime.now().date(),
                    task_time=datetime.datetime.now().time(), user_id=1)
        result = {
            'task_id': todo.id,
            'task_name': todo.task_name,
            'task_content': todo.task_content,
            'task_date': datetime.date.strftime(todo.task_date, '%Y-%m-%d'),
            'task_time': datetime.time.strftime(todo.task_time, '%H:%M')
        }
        self.assertDictEqual(todo.serialize, result)
