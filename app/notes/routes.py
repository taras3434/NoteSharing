from flask import Blueprint, render_template, abort, redirect, url_for, request, send_from_directory
from app.models import db, Note, NoteVersion
import uuid
from flask_login import current_user, login_required
from .forms import CreateNote, EditNote, SearchNote, FilterNote
from sqlalchemy import and_
from datetime import datetime, timezone

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/create-note", methods=["GET", "POST"])
@login_required
def create_note():
    form = CreateNote()
    if form.validate_on_submit():
        user_notes = Note.query.filter_by(user_id=current_user.id)

        note_title = form.title.data
        note_text = form.note.data

        if current_user.check_plan(note_text, user_notes.count()):
            return redirect(url_for("home.pricing"))
        
        note_id = str(uuid.uuid4())
        new_note = Note(id=note_id, 
                        title=note_title, 
                        text=note_text, 
                        user_id=current_user.id,
                        start_date=datetime.now(timezone.utc),
                        last_edit=datetime.now(timezone.utc))
        
        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("notes.view_note", note_id=note_id))
    return render_template("create_note.html", form=form)

@notes_bp.route("/my-notes", methods=["GET", "POST"])
@login_required
def my_notes():
    search_form = SearchNote()
    filter_form = FilterNote(request.args)
    notes = Note.query.filter_by(user_id=current_user.id)
    notes_count = Note.query.filter_by(user_id=current_user.id).count()
    
    search_isActive = False

    if search_form.validate_on_submit():
        notes = Note.query.filter(and_(Note.user_id == current_user.id, 
                                       Note.title.like(f"{search_form.search_field.data.strip()}%")))
        search_isActive = True

    elif filter_form.validate():
        notes = Note.query.filter_by(user_id=current_user.id)
        
        dropdown = {'val1' : notes.order_by(Note.start_date.desc()), 
                    'val2' : notes.order_by(Note.start_date.asc()),
                    'val3' : notes.order_by(Note.title.asc()),
                    'val4' : notes.order_by(Note.title.desc()),
                    'val5' : notes.order_by(Note.is_favorite.desc())}

        notes = dropdown[filter_form.filter_dropdown.data]
    
    return render_template("my_notes.html", 
                           current_user=current_user, 
                           notes=notes, 
                           notes_count=notes_count, 
                           search_form=search_form,
                           filter_form=filter_form, 
                           search_isActive=search_isActive)

@notes_bp.route("/set-favorite", methods=["POST"])
def set_favorite():
    data = request.get_json()
    task_id = data.get('id')
    is_favorite = data.get('is_done')

    note = Note.query.get(task_id)
    if note:
        note.is_favorite = is_favorite
        db.session.commit()

@notes_bp.route("/note/<note_id>", methods=["GET", "POST"])
def view_note(note_id : str):
    form = EditNote()
    note = Note.query.get(note_id)
    note_versions = NoteVersion.query.filter_by(note_id=note_id)

    if form.validate_on_submit():
        
        if form.note.data:
            note_version = NoteVersion(note_id=note.id, 
                                       text=note.text)
            
            db.session.add(note_version)

            note.text = form.note.data
            note.last_edit = datetime.now(timezone.utc)

            if current_user.check_plan(form.note.data):
                return redirect(url_for("home.pricing"))
        elif form.title.data:
            note.title = form.title.data
            note.last_edit = datetime.now(timezone.utc)
        

        db.session.commit()
        
        return redirect(url_for("notes.view_note", 
                                note_id=note_id,
                                note_versions=note_versions))
    
    if note is None:
        abort(404)
    return render_template("note.html", 
                           note=note,
                           note_versions=note_versions,
                           current_user=current_user, 
                           form=form)

@notes_bp.route("/note/<note_id>/delete_note", methods=["POST"])
@login_required
def delete_note(note_id):
    user_note = Note.query.filter_by(id=note_id, 
                                     user_id=current_user.id).first()
    if not user_note:
        abort(403)
    db.session.delete(user_note) 
    db.session.commit()
    return redirect(url_for("notes.my_notes"))
