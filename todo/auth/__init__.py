from flask import Blueprint

from todo.auth.views import login, logout, register

auth = Blueprint('auth', __name__)

auth.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth.add_url_rule('/logout', view_func=logout)
auth.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
