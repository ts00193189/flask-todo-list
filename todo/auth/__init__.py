from flask import Blueprint
from todo.auth.views import login

auth = Blueprint('auth', __name__)

auth.add_url_rule('/login', view_func=login)
