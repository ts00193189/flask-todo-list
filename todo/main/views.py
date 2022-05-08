from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask_login import login_required
from todo.models import User
from todo.models import Todo
from todo.main.utils import DateTimeConverter


def index():
    return render_template('index.html')


@login_required
def create_todo(user_name):
    user = User.query.filter_by(name=user_name).first_or_404()
    task_name = request.form.get('task_name')
    task_content = request.form.get('task_content')
    task_date = request.form.get('task_date')
    task_time = request.form.get('task_time')

    task_date = DateTimeConverter.convert_date(task_date)
    task_time = DateTimeConverter.convert_time(task_time)

    todo = Todo(task_name=task_name, task_content=task_content, task_date=task_date, task_time=task_time,
                user_id=user.id)
    success = todo.save()
    if not success:
        abort(400)

    return jsonify({'msg': 'success'})


@login_required
def get_todos(user_name):
    todo_list = User.query.filter_by(name=user_name).first_or_404().todo_list
    todos = [todo.serialize for todo in todo_list]
    return jsonify({'msg': 'success', 'todos': todos})


@login_required
def update_todo(user_name, task_id):
    todo = Todo.query.filter_by(id=task_id).first_or_404()
    user = User.query.filter_by(name=user_name).first_or_404()
    if todo not in user.todo_list:
        abort(404)

    edit_name = request.form.get('edit_name')
    edit_content = request.form.get('edit_content')
    edit_date = request.form.get('edit_date')
    edit_time = request.form.get('edit_time')

    edit_date = DateTimeConverter.convert_date(edit_date)
    edit_time = DateTimeConverter.convert_time(edit_time)
    if not edit_date or not edit_time:
        abort(400)

    todo.update(edit_name, edit_content, edit_date, edit_time)

    return jsonify({'msg': 'success'})


@login_required
def delete_todo(user_name, task_id):
    todo = Todo.query.filter_by(id=task_id).first_or_404()
    user = User.query.filter_by(name=user_name).first_or_404()
    if todo not in user.todo_list:
        abort(404)
    todo.delete()
    return jsonify({'msg': 'success'})
