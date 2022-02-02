from flask import Blueprint, render_template, url_for

allPosts = Blueprint("allPosts", __name__)

@allPosts.route("/")
def home():
    return render_template("home.html")