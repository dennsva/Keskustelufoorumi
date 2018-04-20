from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.tag.models import Tag
from application.tagging.models import Tagging

from application.tag.forms import TagCreateForm
from application.tag.forms import TagEditForm

@app.route("/tags/", methods=["GET"])
def tag_index():
    return render_template("tag_index.html", tags=Tag.tag_list(), tag_create_form=TagCreateForm())

@app.route("/tags/", methods=["POST"])
def tag_create():
    form = TagCreateForm(request.form)

    if not form.validate():
        return render_template("tag_index.html", tags=Tag.tag_list(), tag_create_form=form)

    tag = Tag(form.name.data)

    db.session().add(tag)
    db.session().commit()

    return render_template("tag_index.html", tags=Tag.tag_list(), tag_create_form=TagCreateForm())

@app.route("/tags/<tag_id>/edit/", methods=["POST"])
def tag_edit_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template("tag_edit.html", tag_edit_form=TagEditForm(), tag=tag)

@app.route("/tags/<tag_id>/edit/post/", methods=["POST"])
def tag_edit(tag_id):
    form = TagEditForm(request.form)
    tag = Tag.query.get(tag_id)

    if not form.validate():
        return render_template("tag_edit.html", tag_edit_form=form, tag=tag)

    tag.name = form.name.data

    db.session().add(tag)
    db.session().commit()
  
    return redirect(url_for("tag_index"))

@app.route("/tags/<tag_id>/delete/", methods=["POST"])
def tag_delete(tag_id):
    tag = Tag.query.get(tag_id)

    Tagging.tag_delete_taggings(tag_id)

    db.session().delete(tag)
    db.session().commit()

    return redirect(url_for("tag_index"))