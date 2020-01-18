from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////carleasingdatabase.db'
app.config['SECRET_KEY'] = 'GITGUDHACCKAZ'
db = SQLAlchemy(app, session_options={
    'expire_on_commit': False,
})

login_manager = LoginManager(app)
migrate = Migrate(app, db)
delim = os.path.sep
static_path = f'{os.getcwd()}{delim}application{delim}flaskcarleasing{delim}static'

MODERATOR_TOKEN = os.environ['MODERATOR_TOKEN']

from users.routes import users
from cars.routes import cars
from concerns.routes import concerns
from main.routes import main
from leasing.routes import leasing


app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(cars, url_prefix='/cars')
app.register_blueprint(concerns, url_prefix='/concerns')
app.register_blueprint(leasing, url_prefix='/leasing')
app.register_blueprint(main)