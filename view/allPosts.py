from flask import Blueprint, render_template, url_for
from models.collection import blogPosts, placeholder
from models.post import example

allPosts = Blueprint("allPosts", __name__)

@allPosts.route("/")
def home():
    if len(blogPosts) == 0:
        return render_template("home.html", allposts = placeholder)

    return render_template("home.html", allposts = blogPosts)