from flask import Blueprint, render_template, redirect, url_for
from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from app.models import User, Note, db
from flask_login import login_user, logout_user, login_required, current_user
from .utils import hash_password, check_password

auth_bp = Blueprint('auth', __name__, template_folder='./templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        registered_user = User(username=form.username.data, password_hash=hash_password(form.password.data))
        db.session.add(registered_user)
        db.session.commit()
        login_user(registered_user)
        return redirect(url_for('home.main', success=True))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if check_password(user.password_hash, password):
            login_user(user)
            return redirect(url_for("home.home"))
    return render_template('login.html', form=form)

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user_notes = Note.query.filter_by(user_id=current_user.id)
    return render_template("profile.html", 
                           current_user=current_user, 
                           user_notes=user_notes)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data

        user = User.query.filter_by(username=current_user.username).first()
        if check_password(user.password_hash, old_password):
            user.password_hash = hash_password(new_password)

            db.session.commit()
            return redirect(url_for("auth.profile"))
        
    return render_template('change_password.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.main"))