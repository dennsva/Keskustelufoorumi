from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.messages.models import Message
from application.messages.forms import MessageCreateForm
from application.messages.forms import MessageEditForm

@app.route("/messages/", methods=["GET"])
def thread():
    return render_template("thread.html", form = MessageCreateForm(), messages = Message.query.all())

@app.route("/messages/edit/<message_id>/", methods=["POST"])
def message_edit_form(message_id):
    message = Message.query.get(message_id)
    return render_template("message_edit.html", form = MessageEditForm(message.text), message = message)

@app.route("/messages/", methods=["POST"])
@login_required
def message_create():
    form = MessageCreateForm(request.form)

    if not form.validate():
        return render_template("thread.html", form = form, messages = Message.query.all())

    m = Message(request.form.get("text"), current_user.id)

    db.session().add(m)
    db.session().commit()
  
    return redirect(url_for("thread"))

@app.route("/messages/edit/<message_id>/post/", methods=["POST"])
def message_edit(message_id):
    form = MessageCreateForm(request.form)

    if not form.validate():
        message = Message.query.get(message_id)
        return render_template("message_edit.html", form=form, message=message)

    m = Message.query.get(message_id)
    m.text = request.form.get("text")
    
    db.session().add(m)
    db.session().commit()

    return redirect(url_for("thread"))

@app.route("/messages/delete/<message_id>", methods=["POST"])
def message_delete(message_id):
    m = Message.query.get(message_id)

    db.session().delete(m)
    db.session().commit()

    return redirect(url_for("thread"))