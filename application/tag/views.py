from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.tag.models import Tag
from application.tagging.models import Tagging

@app.route("/tags/", methods=["GET"])
def tag_index():
    return render_template("tag_index.html", tags=Tag.tag_list())

@app.route("/tags/", methods=["POST"])
def tag_create():

    # FIX VALIDATION
    #if not form.validate():
    #    return render_template("tag_index.html", tags=Tag.tag_list(), tag_create_form=form)

    tag = Tag(request.form.get("name"))

    db.session().add(tag)
    db.session().commit()

    return redirect(url_for('tag_index'))

@app.route("/tags/<tag_id>/delete/", methods=["POST"])
def tag_delete(tag_id):
    tag = Tag.query.get(tag_id)

    Tagging.tag_delete_taggings(tag_id)

    db.session().delete(tag)
    db.session().commit()

    return redirect(url_for("tag_index"))