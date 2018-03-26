from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.messages.models import Message

@app.route("/messages/", methods=["GET"])
def message_index():
    return render_template("messages.html", messages = Message.query.all())

@app.route("/messages/edit/<message_id>/", methods=["POST"])
def message_edit_form(message_id):
    return render_template("message_edit.html", message = Message.query.get(message_id))

@app.route("/messages/", methods=["POST"])
@login_required
def message_create():
    m = Message(request.form.get("text"), current_user.id)

    db.session().add(m)
    db.session().commit()
  
    return redirect(url_for("message_index"))

@app.route("/messages/edit/<message_id>/post/", methods=["POST"])
def message_edit(message_id):
    m = Message.query.get(message_id)
    m.text = request.form.get("text")
    
    db.session().add(m)
    db.session().commit()

    return redirect(url_for("message_index"))

@app.route("/messages/delete/<message_id>", methods=["POST"])
def message_delete(message_id):
    m = Message.query.get(message_id)

    db.session().delete(m)
    db.session().commit()

    return redirect(url_for("message_index"))