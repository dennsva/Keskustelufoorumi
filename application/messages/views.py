from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.messages.models import Message
from application.messages.forms import MessageCreateForm
from application.messages.forms import MessageEditForm
from application.thread.models import Thread

@app.route("/messages/", methods=["GET"])
def message_index():
    return render_template("thread.html", form = MessageCreateForm(), thread = Thread.query.first(), messages=Message.query.all())

@app.route("/threads/<thread_id>/", methods=["GET"])
def thread(thread_id):
    return render_template("thread.html", form = MessageCreateForm(), thread = Thread.query.get(thread_id), messages = db.session().query(Message).filter_by(thread_id = thread_id))

@app.route("/threads/<thread_id>/", methods=["POST"])
@login_required
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