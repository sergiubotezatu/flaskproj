from flask import Blueprint, render_template, url_for
from postRepo.seed import blogPosts, placeholder

home = Blueprint("home", __name__)

@home.route("/")
def frontPage():
    rows = len(blogPosts)
    if rows == 0:
        return render_template("home.html", allposts = placeholder.getPreview())
    
    return render_template("home.html", allposts = blogPosts.getPreview())