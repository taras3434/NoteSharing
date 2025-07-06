from flask import Blueprint, redirect, url_for, render_template

home_bp = Blueprint('home',  __name__, template_folder='./templates')

@home_bp.route("/")
def main():
    return redirect(url_for('home.home'))

@home_bp.route('/home')
def home():
    return render_template("home.html")