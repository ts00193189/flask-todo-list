from flask import Blueprint
from flask import render_template
from todo.main.views import index
from todo.main.errors import page_not_found

main = Blueprint('main', __name__)


main.add_url_rule('/', view_func=index)

main.app_errorhandler(404)(page_not_found)
