from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from application.auth.models import User
from application.auth.forms import UserCreateForm
from application.auth.forms import UserLoginForm

@app.route("/users/", methods=["GET"])
def user_index():
    return render_template("users.html", users = User.query.all())

@app.route("/users/<user_id>/", methods=["GET"])
def user(user_id):
    return render_template("user.html", user = User.query.get(user_id))

@app.route("/users/register/", methods=["GET"])
def user_create_form():
    return render_template("user_create.html", form = UserCreateForm())

@app.route("/users/register/", methods=["POST"])
def user_create():
    form = UserCreateForm(request.form)

    if not form.validate():
        return render_template("user_create.html", form = form)

    user = User(form.username.data, form.password.data)

    db.session().add(user)
    db.session().commit()

    login_user(user)

    return redirect(url_for("index"))

@app.route("/users/login/", methods=["GET"])
def user_login_form():
    return render_template("user_login.html", form = UserLoginForm())

@app.route("/users/login/", methods=["POST"])
def user_login():
    form = UserLoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("user_login.html", form = form, error = "No such username or password")

    login_user(user)

    return redirect(url_for("index"))

@app.route("/users/logout/")
def user_logout():
    logout_user()
    return redirect(url_for("index"))