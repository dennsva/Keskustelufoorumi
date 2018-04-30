from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application.messages.models import Message

from application.thread.models import Thread
from application.auth.models import User

from application.tagging.models import Tagging

from application.tag.models import Tag

from application.read.models import Read

# this is only for debugging purposes
#@app.route("/messages/", methods=["GET"])
#def message_index():
#    return render_template("thread.html", message_create_form=MessageCreateForm(), tagging_create_form=TaggingCreateForm(), thread=Thread.query.first(), messages=Message.query.all(), thread_user=User("Gandalf", "password"))

@app.route("/thread/<thread_id>/", methods=["GET"])
def thread(thread_id, thread_edit=None, message_create=Message("", None, None), show_errors=False, message_edit=None, message_edit_id=None):
    if message_edit_id:
        message_edit_id = int(message_edit_id)
        message_edit = Message.query.get(message_edit_id)

    thread = Thread.query.get(thread_id)
    thread.user = User.query.get(thread.account_id)
    print(thread.user)
    if current_user.is_authenticated:
        Read.mark_as_read(current_user.id, thread_id)

    return render_template("thread.html", 
                            thread=thread,
                            thread_edit=thread_edit,
                            tags=Tag.find_thread_id(thread_id),
                            other_tags=Tag.find_not_thread_id(thread_id),
                            messages=Message.find_thread_id(thread_id),
                            message_create=message_create,
                            show_errors=show_errors,
                            message_edit=message_edit)

@app.route("/thread/<thread_id>/", methods=["POST"])
@login_required(role="ANY")
def message_create(thread_id):
    text = request.form.get("text")
    message = Message(text, current_user.id, thread_id)

    if not message.validate(new=True):
        return thread(thread_id=thread_id, message_create=message, show_errors=True)

    db.session().add(message)
    db.session().commit()
  
    return redirect(url_for('thread', thread_id=thread_id))

@app.route("/thread/edit/<message_id>/", methods=["GET", "POST"])
def message_edit(message_id):
    message = Message.query.get(message_id)

    if request.method == "GET":
        return thread(message.thread_id, message_edit=message)

    message.text = request.form.get("text")

    if not message.validate():
        return thread(message.thread_id, message_edit=message)

    db.session().add(message)
    db.session().commit()
  
    return redirect(url_for('thread', thread_id=message.thread_id))

@app.route("/thread/delete/<message_id>/", methods=["POST"])
def message_delete(message_id):
    message = Message.query.get(message_id)

    db.session().delete(message)
    db.session().commit()

    return redirect(url_for("thread", thread_id=message.thread_id))