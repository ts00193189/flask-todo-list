from todo import create_app
from todo.models import db, User, Todo

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Todo=Todo)