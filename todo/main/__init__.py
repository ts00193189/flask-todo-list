from flask import Blueprint
from todo.main.views import index, create_todo, get_todos
from todo.main.errors import page_not_found

main = Blueprint('main', __name__)


main.add_url_rule('/', view_func=index)
main.add_url_rule('/<user_name>', view_func=create_todo, methods=['POST'])
main.add_url_rule('/<user_name>', view_func=get_todos, methods=['GET'])

main.app_errorhandler(404)(page_not_found)
