import bcrypt
from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user

from application.auth.models import User
from application.auth.forms import UserCreateForm
from application.auth.forms import UserLoginForm

@app.route("/users/", methods=["GET"])
def user_index():
    return render_template("user_index.html", users = User.user_list(), admin_count=User.admin_count())

@app.route("/users/<user_id>/", methods=["GET"])
def user(user_id):
    return render_template("user.html", user = User.query.get(user_id))

@app.route("/users/register/", methods=["GET"])
def user_create_form():
    return render_template("user_create.html", form = UserCreateForm())

@app.route("/users/login/", methods=["GET"])
def user_login_form():
    return render_template("user_login.html", form = UserLoginForm())

@app.route("/users/", methods=["POST"])
def user_create():
    form = UserCreateForm(request.form)

    if not form.validate():
        return render_template("user_create.html", form = form)

    if form.username.data == "deleted":
        return render_template("user_create.html", form = form, error = "Username cannot be deleted")

    user = User.query.filter_by(username=form.username.data, deleted=False).first()
    if user:
        return render_template("user_create.html", form = form, error = "Username already exists")

    password = form.password.data.encode() # utf-8 for bcrypt
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

    user = User(form.username.data, hashed)

    if User.user_count() == 0:
        user.admin = True

    db.session().add(user)
    db.session().commit()

    login_user(user)

    return redirect(url_for("index"))

@app.route("/users/login/", methods=["POST"])
def user_login():
    form = UserLoginForm(request.form)

    if not form.validate():
        return render_template("user_login.html", form = form)

    if form.username.data == "deleted":
        return render_template("user_create.html", form = form, error = "You cannot login to a deleted account")

    user = User.query.filter_by(username=form.username.data, deleted=False).first()
    if not user:
        return render_template("user_login.html", form = form, error = "No such username or password")

    password = request.form.get("password").encode() # utf-8 for bcrypt

    if not bcrypt.checkpw(password, user.password.encode()):
        return render_template("user_login.html", form = form, error = "No such username or password")

    login_user(user)

    return redirect(url_for("index"))

@app.route("/users/logout/")
def user_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/users/<user_id>/toggle/", methods=["POST"])
def user_admin_toggle(user_id):
    user = User.query.get(user_id)

    user.admin = not user.admin

    db.session().commit()

    return redirect(url_for('user_index'))

@app.route("/users/<user_id>/delete/", methods=["POST"])
def user_delete(user_id):
    user = User.query.get(user_id)

    if user.admin and User.admin_count() <= 1:
        redirect(url_for("user_index"))

    if not (current_user.admin or current_user.id == user.id):
        return redirect(url_for('user_index'))

    user.username = "deleted"
    user.password = "deleted"
    user.admin = False
    user.deleted = True

    db.session().commit()

    if user.id == current_user.id:
        logout_user()

    return redirect(url_for("user_index"))