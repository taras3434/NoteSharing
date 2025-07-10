from flask import Blueprint, render_template, abort, redirect, url_for
from app.models import db, Note
import uuid
from flask_login import current_user, login_required
from .forms import CreateNote, EditNote

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/create_note", methods=["GET", "POST"])
def create_note():
    form = CreateNote()
    if form.validate_on_submit():
        if current_user.check_plan(Note.query.filter_by(user_id=current_user.id).count()):
            return redirect(url_for("home.pricing"))
        note_title = form.title.data
        note_text = form.note.data
        note_id = str(uuid.uuid4())
        new_note = Note(id=note_id, title=note_title, text=note_text, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for("notes.view_note", note_id=note_id))
    return render_template("create_note.html", form=form)

@notes_bp.route("/my_notes")
@login_required
def my_notes():
    user_notes = Note.query.filter_by(user_id=current_user.id)
    return render_template("my_notes.html", current_user=current_user, user_notes=user_notes)

@notes_bp.route("/note/<note_id>/delete_note", methods=["POST"])
@login_required
def delete_note(note_id):
    user_note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not user_note:
        abort(403)
    db.session.delete(user_note) 
    db.session.commit()
    return redirect(url_for("notes.my_notes"))
        
@notes_bp.route("/note/<note_id>", methods=["GET", "POST"])
def view_note(note_id : str):
    form = EditNote()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.text = form.note.data
        db.session.commit()
        return redirect(url_for("notes.view_note", note_id=note_id))
    
    if note is None:
        abort(404)
    return render_template("note.html", note=note, current_user=current_user, form=form)
