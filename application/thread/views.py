from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.thread.models import Thread
from application.thread.forms import ThreadCreateForm
from application.thread.forms import ThreadEditForm

@app.route("/threads/", methods=["GET"])
def thread_index():
    return render_template("thread_index.html", threads = Thread.query.all())

@app.route("/threads/", methods=["POST"])
@login_required
def thread_create():
    form = ThreadCreateForm(request.form)

    if not form.validate():
        return render_template("thread_create.html", form = form)

    thread = Thread(request.form.get("subject"), request.form.get("text"), current_user.id)

    db.session().add(thread)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id = thread.id))

@app.route("/threads/new/", methods=["POST"])
def thread_create_form():
    return render_template("thread_create.html", form = ThreadCreateForm())

@app.route("/threads/<thread_id>/edit/", methods=["POST"])
def thread_edit_form(thread_id):
    thread = Thread.query.get(thread._id)
    return render_template("thread_edit.html", form = ThreadEditForm(thread.text), thread = thread)