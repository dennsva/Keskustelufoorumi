from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application.thread.models import Thread
from application.tag.models import Tag
from application.tagging.models import Tagging
from application.messages.models import Message

from application.messages.views import thread as view_thread

@app.route("/threads/", methods=["GET"])
def thread_index(threads=Thread.thread_list(), thread_create=Thread("", "", None), show_errors=False, search_text=None, tag=None):
    return render_template("thread_index.html",
                            threads=threads,
                            thread_create=thread_create,
                            show_errors=show_errors,
                            search_text=search_text,
                            tag=tag)

@app.route("/threads/search/", methods=["POST"])
def thread_search():
    search_text=request.form.get("text")
    return thread_index(threads=Thread.search(search_text), search_text=search_text)

@app.route("/threads/tag/<tag_id>/", methods=["GET"])
def thread_find_tag_id(tag_id):
    return thread_index(threads=Thread.find_tag_id(tag_id), tag=Tag.query.get(tag_id))

@app.route("/threads/", methods=["POST"])
@login_required
def thread_create():
    thread = Thread(request.form.get("subject"), request.form.get("text"), current_user.id)

    if not thread.validate():
        return thread_index(thread_create=thread, show_errors=True)

    db.session().add(thread)
    db.session().commit()
  
    return redirect(url_for('thread', thread_id=thread.id))

@app.route("/thread/<thread_id>/edit/", methods=["GET", "POST"])
def thread_edit(thread_id):
    thread = Thread.query.get(thread_id)

    if request.method == "GET":
        return view_thread(thread_id, thread_edit=thread)

    thread.text = request.form.get("text")

    if not thread.validate():
        return view_thread(thread_id, thread_edit=thread)

    db.session().add(thread)
    db.session().commit()
  
    return redirect(url_for('thread', thread_id=thread_id))

@app.route("/threads/<thread_id>/delete/", methods=["POST"])
def thread_delete(thread_id):
    thread = Thread.query.get(thread_id)

    Message.thread_delete_messages(thread_id)
    Tagging.thread_delete_taggings(thread_id)

    db.session().delete(thread)
    db.session().commit()

    return redirect(url_for("thread_index"))