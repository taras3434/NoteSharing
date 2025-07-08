from flask import Blueprint, render_template, request, abort, redirect, url_for
from app.models import db, Note
import uuid
from flask_login import current_user, login_required
from .forms import CreateNote

notes_bp = Blueprint('notes', __name__, template_folder='./templates')

@notes_bp.route("/create_note", methods=["GET", "POST"])
def create_note():
    form = CreateNote()
    if form.validate_on_submit():
        note_text = form.note.data
        note_id = str(uuid.uuid4())
        new_note = Note(id=note_id, text=note_text, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for("notes.view_note", note_id=note_id))
    return render_template("create_note.html", form=form)

@notes_bp.route("/my_notes")
@login_required
def my_notes():
    user_notes = Note.query.filter_by(user_id=current_user.id)
    return render_template("my_notes.html", current_user=current_user, user_notes=user_notes)

@notes_bp.route("/note/<note_id>")
def view_note(note_id : str):
    note = Note.query.get(note_id)
    if note is None:
        abort(404)
    return render_template("note.html", note=note, current_user=current_user)
