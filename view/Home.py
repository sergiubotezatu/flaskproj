from flask import Blueprint, render_template, current_app
from services import seed, posts_factory

home = Blueprint("home", __name__)
source_factory = posts_factory.Create(current_app.config["TESTING"])
blogPosts = source_factory.create_source

@home.route("/")
def front_page():
    rows = len(blogPosts)
    if rows == 0:
        return render_template("home.html", allposts = seed.placeholder.get_preview())

    return render_template("home.html", allposts = blogPosts.get_preview())
