from flask import Blueprint, render_template, redirect, url_for
from .forms import RegistrationForm, LoginForm
from app.models import User, db
from flask_login import current_user, login_user, logout_user


auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        registered_user = User(username=form.username.data, password_hash=form.password.data)
        db.session.add(registered_user)
        db.session.commit()
        return redirect(url_for('main.main', success=True))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        registered_user = User(username=form.username.data, password_hash=form.password.data)
        db.session.add(registered_user)
        db.session.commit()
        return redirect(url_for('main.main', success=True))
    return render_template('register.html', form=form)
