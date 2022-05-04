from flask import Blueprint
from todo.auth.views import login
from todo.auth.views import logout

auth = Blueprint('auth', __name__)

auth.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth.add_url_rule('/logout', view_func=logout)
