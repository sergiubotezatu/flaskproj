from flask import Blueprint, render_template
from services import seed

home = Blueprint("home", __name__)
blogPosts = seed.source_factory.create_source()

@home.route("/")
def front_page():
    rows = len(blogPosts)
    if rows == 0:
        return render_template("home.html", allposts = seed.placeholder.get_preview())

    return render_template("home.html", allposts = blogPosts.get_preview())
