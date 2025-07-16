from flask import Blueprint, redirect, url_for, render_template, current_app
import json
import os
from .utils import load_json

home_bp = Blueprint('home',  __name__, template_folder='./templates')

@home_bp.route("/")
def main():
    return redirect(url_for('home.home'))

@home_bp.route('/home')
def home():
    return render_template("home.html")

@home_bp.route("/pricing")
def pricing():
    return render_template("pricing.html")

@home_bp.route("/terms-of-use")
def terms_of_use():
    terms_sections = load_json("terms_of_use.json")
    return render_template("terms_of_use.html", terms_sections=terms_sections)

@home_bp.route("/privacy-policy")
def privacy_policy():
    privacy_sections = load_json("terms_of_use.json")

    return render_template("privacy_policy.html", privacy_sections=privacy_sections)