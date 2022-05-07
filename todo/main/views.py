from flask import render_template
from flask import request
from flask import jsonify
from todo.models import User
from todo.models import Todo
from todo.main.utils import DateTimeConverter


def index():
    return render_template('index.html')


def create_todo(user_name):
    user = User.query.filter_by(name=user_name).first()
    task_name = request.form.get('task_name')
    task_content = request.form.get('task_content')
    task_date = request.form.get('task_date')
    task_time = request.form.get('task_time')

    task_date = DateTimeConverter.convert_date(task_date)
    task_time = DateTimeConverter.convert_time(task_time)

    todo = Todo(task_name=task_name, task_content=task_content, task_date=task_date, task_time=task_time,
                user_id=user.id)
    todo.save()
    return jsonify({'msg': 'success'})


def get_todos(user_name):
    todo_list = User.query.filter_by(name=user_name).first().todo_list
    todos = [todo.serialize for todo in todo_list]
    return jsonify({'msg': 'success', 'todos': todos})


def get_todo():
    pass


def update_todo():
    pass


def delete_todo(user_name, task_id):
    todo = Todo.query.filter_by(id=task_id).first_or_404()
    todo.delete()
    return jsonify({'msg': 'success'})




