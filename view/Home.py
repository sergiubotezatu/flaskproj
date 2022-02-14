from flask import Blueprint, current_app, render_template
from postRepo.seed import blogPosts, placeholder

home = Blueprint("home", __name__)

@home.route("/")
def front_page():
    rows = len(blogPosts)
    if rows == 0:
        return render_template("home.html", allposts = placeholder.get_preview())

    return render_template("home.html", allposts = blogPosts.get_preview())
