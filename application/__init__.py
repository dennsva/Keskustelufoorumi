from flask import Flask
app = Flask(__name__)

# database
from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "user_login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# application

from application.auth import models
from application.tag import models
from application.messages import models
from application.thread import models
from application.read import models
from application.tagging import models

# create database tables
try:
    db.create_all()
except:
    pass

# views
from application import views
from application.auth import views
from application.tag import views
from application.messages import views
from application.thread import views
from application.tagging import views

# more login functionality
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)