from flask import Flask
app = Flask(__name__)
from application.auth.models import User
from application.messages.models import Message
from application.thread.models import Thread

# database
from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# application
from application import views

from application.messages import models
from application.messages import views

from application.auth import models
from application.auth import views

from application.thread import models
from application.thread import views

# login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "user_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# create database tables
try:
    db.create_all()
except:
    pass

# create default user

user = User("dennis", "moi")
db.session().add(user)
db.session().commit()

# create default thread

thread = Thread("hello world", "this is a default thread", User.query.first())
db.session().add(thread)
db.session().commit()

# create default message

message = Message("hello", User.query.first(), Thread.query.first())
db.session().add(message)
db.session().commit()