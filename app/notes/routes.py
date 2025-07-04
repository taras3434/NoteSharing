from flask import Blueprint, render_template, request, abort
from app.models import db, Note
import uuid
from flask_login import current_user

notes_bp = Blueprint('notes', __name__, template_folder='./templates')

@notes_bp.route("/")
def main():
    success = request.args.get("success")

    return render_template("index.html", success=success)

@notes_bp.route("/create_note", methods=["POST"])
def create_note():
    note_text = request.form.get("note_text")
    note_id = None
    if note_text:
        note_id = str(uuid.uuid4())  # Generate a unique id
        new_note = Note(id=note_id, 
                        text=note_text)
        db.session.add(new_note)
        db.session.commit()
    return render_template("create_note.html", note_id=note_id)

@notes_bp.route("/note/<note_id>")
def view_note(note_id : str):
    note = Note.query.get(note_id).text
    if note is None:
        abort(404)
    return render_template("note.html", note=note)