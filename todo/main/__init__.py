from flask import Blueprint

from todo.main.errors import bad_request, page_not_found
from todo.main.views import (create_todo, delete_todo, get_todos, index,
                             update_todo)

main = Blueprint('main', __name__)


main.add_url_rule('/', view_func=index)
main.add_url_rule('/<user_name>', view_func=create_todo, methods=['POST'])
main.add_url_rule('/<user_name>', view_func=get_todos, methods=['GET'])
main.add_url_rule('/<user_name>/<int:task_id>',
                  view_func=delete_todo, methods=['DELETE'])
main.add_url_rule('/<user_name>/<int:task_id>',
                  view_func=update_todo, methods=['PUT'])

main.app_errorhandler(404)(page_not_found)
main.app_errorhandler(400)(bad_request)
