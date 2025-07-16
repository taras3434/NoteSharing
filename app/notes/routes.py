from flask import Blueprint, render_template, abort, redirect, url_for, request, jsonify
from app.models import db, Note, NoteVersion, Tag, User
import uuid
from flask_login import current_user, login_required
from .forms import CreateNote, EditNote
from sqlalchemy import and_
from datetime import datetime, timezone

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/create-note", methods=["GET", "POST"])
@login_required
def create_note():
    form = CreateNote()
    user_tags = Tag.query.filter_by(user_id=current_user.id)

    if form.validate_on_submit():
        selected_ids = request.form.get("selected_tags", "")
        tag_ids = [int(i) for i in selected_ids.split(",") if i.isdigit()]

        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        
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
                        tags=tags,
                        start_date=datetime.now(timezone.utc),
                        last_edit=datetime.now(timezone.utc))
        
        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("notes.view_note", note_id=note_id, user_tags=user_tags))
    return render_template("create_note.html", form=form, user_tags=user_tags)


@notes_bp.route('/add-tag', methods=['POST'])
@login_required
def add_tag():
    data = request.get_json()
    tag_name = data.get('name', '').strip()

    if not tag_name:
        return jsonify({'error': 'Empty tag'}), 400

    existing_tag = Tag.query.filter_by(name=tag_name, user_id=current_user.id).first()
    if existing_tag:
        return jsonify({'error': 'Tag already exists'}), 400

    new_tag = Tag(name=tag_name, user_id=current_user.id)
    db.session.add(new_tag)
    db.session.commit()

    return jsonify({'message': 'Tag added', 'tag': {'id': new_tag.id, 'name': new_tag.name}})

@notes_bp.route("/my-notes", methods=["GET", "POST"])
@login_required
def my_notes():
    notes = Note.query.filter_by(user_id=current_user.id)
    notes_count = Note.query.filter_by(user_id=current_user.id).count()
    user_tags = Tag.query.filter_by(user_id=current_user.id)

    search_term = request.args.get("search_field", "").strip()
    selected_tags_str = request.args.get("selected_tags", "")
    selected_tag_ids = [int(tid) for tid in selected_tags_str.split(',') if tid.isdigit()]
    search_isActive = False

    # Filter by search query
    if search_term:
        notes = notes.filter(Note.title.ilike(f"{search_term}%"))
        search_isActive = True

    # Filter by selected tags
    if selected_tag_ids:
        for tag_id in selected_tag_ids:
            notes = notes.filter(Note.tags.any(Tag.id == tag_id))
        search_isActive = True
                
    selected_filter = request.args.get("filter_dropdown")  
    if selected_filter:
        dropdown = {'val1' : notes.order_by(Note.start_date.desc()), 
                    'val2' : notes.order_by(Note.start_date.asc()),
                    'val3' : notes.order_by(Note.title.asc()),
                    'val4' : notes.order_by(Note.title.desc()),
                    'val5' : notes.order_by(Note.is_favorite.desc())}

        notes = dropdown[selected_filter]
    
    return render_template("my_notes.html", 
                           current_user=current_user, 
                           notes=notes, 
                           notes_count=notes_count,
                           user_tags=user_tags,
                           search_isActive=search_isActive,
                           selected_tag_ids=selected_tag_ids)

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
    
    version_id = request.args.get("version_id", type=int)
    if version_id:
        version = NoteVersion.query.get(version_id)
        if version and version.note_id == note_id:
            note.text = version.text
            
    if form.validate_on_submit():
        
        if form.note.data:
            note_version = NoteVersion(note_id=note.id, 
                                       text=note.text,
                                       version_date=note.last_edit)
            
            db.session.add(note_version)

            note.text = form.note.data
            note.last_edit = datetime.now(timezone.utc)

            if current_user.check_plan(form.note.data):
                return redirect(url_for("home.pricing"))
        elif form.new_editor.data:
            note = Note.query.get(note_id)
            user = User.query.filter_by(username=form.new_editor.data).first()
            
            if not user:
                form.new_editor.errors.append('Username does not exist')
            elif user in note.editors:
                form.new_editor.errors.append('Username already editor')

            else:
                note.editors.append(user)
            
        elif form.title.data:
            note.title = form.title.data
            note.last_edit = datetime.now(timezone.utc)
        

        db.session.commit()
    
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
