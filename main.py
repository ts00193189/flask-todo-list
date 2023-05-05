import unittest

from flask_migrate import Migrate

from todo import create_app
from todo.models import Todo, User, db

app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Todo": Todo}


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
