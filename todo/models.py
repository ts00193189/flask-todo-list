import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from todo import login_manager
from todo import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, index=True)
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
        return '<User "{}">'.format(self.name)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200))
    task_content = db.Column(db.Text)
    task_date = db.Column(db.Date)
    task_time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Todo "{}">'.format(self.task_name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, task_name, task_content, task_date, task_time):
        self.task_name = task_name
        self.task_content = task_content
        self.task_date = task_date
        self.task_time = task_time
        self.save()

    @property
    def serialize(self):
        data = {
            'task_id': self.id,
            'task_name': self.task_name,
            'task_content': self.task_content,
            'task_date': datetime.date.strftime(self.task_date, '%Y-%m-%d'),
            'task_time': datetime.time.strftime(self.task_time, '%H:%M')
        }
        return data


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))