from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application.tag.models import Tag
from application.tagging.models import Tagging

@app.route("/tags/", methods=["GET"])
def tag_index(tag_create=Tag(""), show_errors=False):
    return render_template("tag_index.html",
                            tags=Tag.tag_list(),
                            tag_create=tag_create,
                            show_errors=show_errors)

@app.route("/tags/", methods=["POST"])
@login_required(role="ANY")
def tag_create():
    tag = Tag(request.form.get("name"))

    if not current_user.admin:
        return redirect(url_for("tag_index"))

    if not tag.validate(new=True):
        return tag_index(tag_create=tag, show_errors=True)

    db.session().add(tag)
    db.session().commit()

    return redirect(url_for('tag_index'))

@app.route("/tags/<tag_id>/delete/", methods=["POST"])
@login_required(role="ANY")
def tag_delete(tag_id):
    tag = Tag.query.get(tag_id)

    if not current_user.admin:
        return redirect(url_for("tag_index"))

    Tagging.tag_delete_taggings(tag_id)

    db.session().delete(tag)
    db.session().commit()

    return redirect(url_for("tag_index"))