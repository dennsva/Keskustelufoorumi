from application import app, db
from flask import redirect, render_template, request, url_for
from application.users.models import User
from application.users.forms import UserCreateForm

@app.route("/users/", methods=["GET"])
def users_index():
    return render_template("users.html", users = User.query.all())

@app.route("/users/<user_id>/", methods=["GET"])
def user(user_id):
    return render_template("user.html", user = User.query.get(user_id))

@app.route("/users/register/")
def user_edit_form():
    return render_template("user_create.html", form = UserCreateForm())

@app.route("/users/register/", methods=["POST"])
def user_create():
    form = UserCreateForm(request.form)

    if not form.validate():
        return render_template("user_create.html", form = form)

    u = User(form.username.data, form.password.data)

    db.session().add(u)
    db.session().commit()

    return redirect(url_for("users_index"))