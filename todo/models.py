import datetime

from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable=False)
    todo_list = db.relationship('Todo', backref='user')

    @property
    def password(self):  # pylint: disable=function-redefined
        raise AttributeError('Password is write-only attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User "{self.name}"'


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    task_content = db.Column(db.Text, nullable=False)
    task_date = db.Column(db.Date, nullable=False)
    task_time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Todo "{self.task_name}"'

    def save(self):
        user_ids = [user.id for user in User.query.all()]
        if self.user_id not in user_ids:
            return False
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:  # pylint: disable=broad-exception-caught
            db.session.rollback()
            return False
        return True

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:  # pylint: disable=broad-exception-caught
            db.session.rollback()
            return False
        return True

    def update(self, task_name, task_content, task_date, task_time):
        self.task_name = task_name
        self.task_content = task_content
        self.task_date = task_date
        self.task_time = task_time
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:  # pylint: disable=broad-exception-caught
            db.session.rollback()
            return False
        return True

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
