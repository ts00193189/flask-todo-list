import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'set your key in env'
    BOOTSTRAP_BOOTSWATCH_THEME = 'flatly'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'dev_db.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test_db.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}