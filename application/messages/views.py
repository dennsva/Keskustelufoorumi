from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application.messages.models import Message
from application.messages.forms import MessageCreateForm
from application.messages.forms import MessageEditForm

from application.thread.models import Thread
from application.auth.models import User

from application.tagging.models import Tagging
from application.tagging.forms import TaggingCreateForm

from application.tag.models import Tag

@app.route("/messages/", methods=["GET"])
def message_index():
    return render_template("thread.html", message_create_form=MessageCreateForm(), tagging_create_form=TaggingCreateForm(), thread=Thread.query.first(), messages=Message.query.all(), thread_user=User("Gandalf", "password"))

@app.route("/threads/<thread_id>/", methods=["GET"])
def thread(thread_id, **params):
    message_create_text = ""
    message_edit_text = None
    tagging = None
    message_edit_id = None
    message_create_errors = []
    message_edit_errors = []
    if ("message_edit_id" in params):
        message_edit_id=int(params["message_edit_id"])
    if ("message_create_text" in params):
        message_create_text=params["message_create_text"]
    if ("message_edit_text" in params):
        message_edit_text=params["message_edit_text"]
    elif(message_edit_id):
        message_edit_text=Message.query.get(message_edit_id).text
    if ("message_create_errors" in params):
        message_create_errors=params["message_create_errors"]
    if ("message_edit_errors" in params):
        message_edit_errors=params["message_edit_errors"]
    if ("tagging" in params):
        tagging=params["tagging"]

    thread = Thread.query.get(thread_id)
    thread_user = User.query.get(thread.account_id)

    return render_template("thread.html", thread=thread, thread_user=thread_user, message_create_text=message_create_text, message_create_errors=message_create_errors, tagging=tagging, messages=Message.find_thread_id(thread_id), tags=Tag.find_thread_id(thread_id), message_edit_id=message_edit_id, message_edit_text=message_edit_text, message_edit_errors=message_edit_errors)

@app.route("/threads/<thread_id>/", methods=["POST"])
@login_required(role="ANY")
def message_create(thread_id):
    text = request.form.get("text")

    message = Message(text, current_user.id, thread_id)

    if not message.validate():
        return thread(thread_id, text=text, message_create_errors=message.errors())

    db.session().add(message)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread_id))

@app.route("/messages/<message_id>/edit/", methods=["POST"])
def message_edit_form(message_id):
    message = Message.query.get(message_id)
    return thread(message.thread_id, message_edit_id=message_id)

@app.route("/messages/<message_id>/edit/post/", methods=["POST"])
def message_edit(message_id):
    message = Message.query.get(message_id)
    message.text = request.form.get("text")

    if not message.validate():
        return thread(message.thread_id, message_edit_id=message_id, message_edit_text=message.text, message_edit_errors=message.errors())

    db.session().add(message)
    db.session().commit()
  
    return thread(message.thread_id)

@app.route("/messages/<message_id>/delete/", methods=["POST"])
def message_delete(message_id):
    message = Message.query.get(message_id)

    db.session().delete(message)
    db.session().commit()

    return redirect(url_for("thread", thread_id=message.thread_id))