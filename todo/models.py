from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from todo import login_manager
from todo import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    todo_list = db.relationship('Todo', backref='user')

    @property
    def password(self):
        raise AttributeError('Password is write-only attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    task_content = db.Column(db.Text)
    task_datetime = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Todo {}>'.format(self.task)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))