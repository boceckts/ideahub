import os

basedir = os.path.abspath(os.path.dirname(__file__))


def of_env():
    env = os.getenv('FLASK_ENV') or 'testing'
    if env.lower().startswith('production'):
        return ProductionConfig
    elif env.lower().startswith('development'):
        return DevelopmentConfig
    else:
        return TestingConfig


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    extend_existing = True
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
