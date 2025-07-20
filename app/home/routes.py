from flask import Blueprint, redirect, url_for, render_template
from .utils import load_json

# Define the 'home' blueprint
home_bp = Blueprint('home',  __name__)

@home_bp.route("/")
def main():
    """
    Redirect the root URL '/' to the '/home' page
    """
    return redirect(url_for('home.home'))

@home_bp.route('/home')
def home():
    """
    Home page render
    """
    faqs = load_json("faq.json")

    return render_template("home.html", faqs=faqs)

@home_bp.route("/pricing")
def pricing():
    """
    Pricing information render
    """
    return render_template("pricing.html")

@home_bp.route("/terms-of-use")
def terms_of_use():
    """
    Load terms of use content from a JSON file and render the terms of use page
    """
    terms_sections = load_json("terms_of_use.json")
    return render_template("terms_of_use.html", terms_sections=terms_sections)

@home_bp.route("/privacy-policy")
def privacy_policy():
    """
    Load privacy policy content from a JSON file and render the privacy policy page
    """
    privacy_sections = load_json("privacy_policy.json")

    return render_template("privacy_policy.html", privacy_sections=privacy_sections)