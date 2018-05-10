from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.tagging.models import Tagging

from sqlalchemy.sql import text

@app.route("/threads/<thread_id>/tag/", methods=["POST"])
@login_required
def tagging_create(thread_id):

    tagging = Tagging(thread_id, request.form.get("id"), current_user.id)

    if not tagging.validate(new=True):
        return redirect(url_for('thread', thread_id=thread_id))

    db.session().add(tagging)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread_id))

@app.route("/tagging/delete/<tag_id>/<thread_id>/", methods=["POST"])
def tagging_delete(tag_id, thread_id):

    if not tag_id:
        return "no tag_id"

    if not thread_id:
        return "no thread_id"

    stmt = text("DELETE FROM Tagging"
                " WHERE Tagging.tag_id=:tag_id"
                " AND Tagging.thread_id=:thread_id").params(tag_id=tag_id, thread_id=thread_id)

    db.engine.execute(stmt)

    return redirect(url_for("thread", thread_id=thread_id))

@app.route("/tagging/<tag_id>/<thread_id>/", methods=["POST"])
def tagging_button(tag_id, thread_id):

    if "delete" in request.form:
        if current_user.is_authenticated:
            return tagging_delete(tag_id, thread_id)
        else:
            return redirect(url_for("thread", thread_id=thread_id))

    return redirect(url_for("thread_find_tag_id", tag_id=tag_id))