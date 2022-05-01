from flask import Flask

from todo import todo_bp
from todo.models import db

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

app.register_blueprint(todo_bp, url_prefix='/todo')


if __name__ == '__main__':
    app.debug = True
    app.run()