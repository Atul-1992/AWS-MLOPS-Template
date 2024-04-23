from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from projects.project_1 import project_1_bp

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'random_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

login_manager = LoginManager()
db = SQLAlchemy(app)
Migrate(app, db)
login_manager.init_app(app=app)
login_manager.login_view = 'login'