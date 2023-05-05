from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

from config import config
from todo.auth import auth
from todo.main import main

from .models import db, login_manager

bootstrap = Bootstrap5()
csrf = CSRFProtect()


def create_app(config_name='development'):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main, url_prefix='/todo')

    return app
