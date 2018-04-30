from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.tagging.models import Tagging

@app.route("/threads/<thread_id>/tag/", methods=["POST"])
@login_required
def tagging_create(thread_id):

    tagging = Tagging(thread_id, request.form.get("id"), current_user.id)

    if not tagging.validate(new=True):
        return redirect(url_for('thread', thread_id=thread_id))

    db.session().add(tagging)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread_id))