from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.thread.models import Thread
from application.messages.models import Message
from application.thread.forms import ThreadCreateForm
from application.thread.forms import ThreadEditForm
from application.thread.forms import ThreadSearchForm

@app.route("/threads/", methods=["GET"])
def thread_index():
    return render_template("thread_index.html", threads=Thread.thread_list(), thread_search_form=ThreadSearchForm())

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
    thread = Thread.query.get(thread_id)
    return render_template("thread_edit.html", form = ThreadEditForm(thread.text), thread = thread)

@app.route("/threads/<thread_id>/edit/post/", methods=["POST"])
def thread_edit(thread_id):
    form = ThreadEditForm(request.form)

    if not form.validate():
        thread = Thread.query.get(thread_id)
        return render_template("thread_create.html", form = form, thread=thread)

    thread = Thread.query.get(thread_id)
    thread.subject = form.subject.data
    thread.text = form.text.data

    db.session().add(thread)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread.id))

@app.route("/threads/search/<search_text>/", methods=["GET"])
def thread_search(search_text):
    return render_template("thread_index.html", search_text=search_text, threads = Thread.search_thread(search_text), thread_search_form=ThreadSearchForm())

@app.route("/threads/search/", methods=["POST"])
def thread_search_post():
    form = ThreadSearchForm(request.form)
    return redirect(url_for("thread_search", search_text=form.search_text.data))

@app.route("/threads/<thread_id>/delete/", methods=["POST"])
def thread_delete(thread_id):
    thread = Thread.query.get(thread_id)

    Message.thread_delete_messages(thread_id)

    db.session().delete(thread)
    db.session().commit()

    return redirect(url_for("thread_index"))