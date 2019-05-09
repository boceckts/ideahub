from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

import config

app = Flask(__name__)
app.config.from_object(config.of_env())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)

from app.errors import internal_error
from app import views, errors
from app.api import api
from app.db_initializer import initdb
