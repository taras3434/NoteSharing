from flask import Blueprint, render_template, abort, redirect, url_for, request
from app.models import db, Note, NoteVersion, User
import uuid
from flask_login import current_user, login_required
from .forms import CreateNote, EditNote
from sqlalchemy import or_, func
from datetime import datetime, timezone

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/create-note", methods=["GET", "POST"])
@login_required
def create_note():
    """
    Handle creation of a new note.
    """
    form = CreateNote()

    if form.validate_on_submit():
        note_title = form.title.data
        note_text = form.note.data
        
        # Create new note with a unique UUID
        note_id = str(uuid.uuid4())
        new_note = Note(id=note_id, 
                        title=note_title, 
                        text=note_text, 
                        user_id=current_user.id,
                        start_date=datetime.now(timezone.utc),
                        last_edit=datetime.now(timezone.utc))
        
        db.session.add(new_note)
        db.session.commit()
        
        # Redirect to view the newly created note
        return redirect(url_for("notes.note", note_id=note_id))
    
    # Render note creation page
    return render_template("create_note.html", form=form)

@notes_bp.route("/my-notes", methods=["GET", "POST"])
@login_required
def my_notes():
    """
    Display the list of notes for the logged-in user.
    """
    notes = Note.query.filter_by(user_id=current_user.id)
    notes_count = Note.query.filter_by(user_id=current_user.id).count()

    search_term = request.args.get("search_field", "").strip()
    search_isActive = False

    # Filter notes by search
    if search_term:
        notes = notes.filter(or_(Note.title.ilike(f"%{search_term}%"), Note.text.ilike(f"%{search_term}%")))
        search_isActive = True

    # Apply filter            
    selected_filter = request.args.get("filter_dropdown")  
    if selected_filter:
        dropdown = {
            'val1': notes.order_by(Note.start_date.desc()),
            'val2': notes.order_by(Note.start_date.asc()),
            'val3': notes.order_by(func.lower(Note.title).asc()),
            'val4': notes.order_by(func.lower(Note.title).desc()),
            'val5': notes.order_by(Note.is_favorite.desc())
        }

        notes = dropdown[selected_filter]

    # Render the notes list page
    return render_template("my_notes.html", 
                           current_user=current_user, 
                           notes=notes, 
                           notes_count=notes_count,
                           search_isActive=search_isActive
                           )

@notes_bp.route("/set-favorite", methods=["POST"])
@login_required
def set_favorite():
    """
    Toggle favorite status for a note
    """
    data = request.get_json()
    note_id = data.get('id')
    is_favorite = data.get('is_done')

    note = Note.query.get(note_id)
    if note:
        note.is_favorite = is_favorite
        db.session.commit()

@notes_bp.route("/note/<note_id>", methods=["GET", "POST"])
def note(note_id):
    """
    Display a single note
    """
    form = EditNote()
    note = Note.query.get(note_id)
    note_versions = NoteVersion.query.filter_by(note_id=note_id)
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.start_date.desc())

    if note is None:
        abort(404)

    # Restore a specific version of the note
    version_id = request.args.get("version_id", type=int)
    if version_id:
        version = NoteVersion.query.get(version_id)
        if version and version.note_id == note_id:
            note.text = version.text
            
    if form.validate_on_submit():

        # Handle note text update
        if form.note.data:

            # Save current note text as a version
            note_version = NoteVersion(note_id=note.id, 
                                       text=note.text,
                                       version_date=note.last_edit)
            
            db.session.add(note_version)

            note.text = form.note.data
            note.last_edit = datetime.now(timezone.utc)
        
        # Handle note title update   
        elif form.title.data:
            note.title = form.title.data
            note.last_edit = datetime.now(timezone.utc)
        
        db.session.commit()
    
    return render_template("note.html", 
                           note=note,
                           note_versions=note_versions,
                           current_user=current_user, 
                           form=form,
                           notes=notes)

@notes_bp.route("/note/<note_id>/delete_note", methods=["POST"])
@login_required
def delete_note(note_id):
    """
    Deletes a note owned by the current user.
    """
    user_note = Note.query.filter_by(id=note_id, 
                                     user_id=current_user.id).first()
    if not user_note:
        abort(404)
    db.session.delete(user_note) 
    db.session.commit()
    return redirect(url_for("notes.my_notes"))
