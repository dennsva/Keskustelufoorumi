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
def thread(thread_id):
    thread = Thread.query.get(thread_id)
    thread_user = User.query.get(thread.account_id)
    return render_template("thread.html", thread=thread, thread_user=thread_user, message_create_form=MessageCreateForm(), tagging_create_form=TaggingCreateForm(), messages=Message.find_thread_id(thread_id), tags=Tag.find_thread_id(thread_id))

@app.route("/threads/<thread_id>/", methods=["POST"])
@login_required(role="ANY")
def message_create(thread_id):
    form = MessageCreateForm(request.form)

    if not form.validate():
        return render_template("thread.html", form = form, messages = Message.query.all())

    m = Message(form.text.data, current_user.id, thread_id)

    db.session().add(m)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread_id))

@app.route("/messages/<message_id>/edit/", methods=["POST"])
def message_edit_form(message_id):
    message = Message.query.get(message_id)
    return render_template("message_edit.html", form=MessageEditForm(message.text), message=message)

@app.route("/messages/<message_id>/edit/post/", methods=["POST"])
def message_edit(message_id):
    form = MessageEditForm(request.form)

    if not form.validate():
        message = Message.query.get(message_id)
        return render_template("message_edit.html", form=form, message=message)

    message = Message.query.get(message_id)
    message.text = form.text.data
    
    db.session().add(message)
    db.session().commit()

    return redirect(url_for("thread", thread_id=message.thread_id))

@app.route("/messages/<message_id>/delete/", methods=["POST"])
def message_delete(message_id):
    message = Message.query.get(message_id)

    db.session().delete(message)
    db.session().commit()

    return redirect(url_for("thread", thread_id=message.thread_id))