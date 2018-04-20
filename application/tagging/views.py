from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.tagging.models import Tagging
from application.tagging.forms import TaggingCreateForm

@app.route("/threads/<thread_id>/tag/", methods=["POST"])
@login_required
def tagging_create(thread_id):
    form = TaggingCreateForm(request.form)

    tagging = Tagging(thread_id, form.id.data, current_user.id)

    db.session().add(tagging)
    db.session().commit()
  
    return redirect(url_for("thread", thread_id=thread_id))
