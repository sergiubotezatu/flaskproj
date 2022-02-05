from flask import Blueprint, render_template, url_for
from postRepo.blogPosts import blogPosts, placeholder
from models.post import example

home = Blueprint("allPosts", __name__)

@home.route("/")
def home():
    rows = len(blogPosts)
    if rows == 0:
        return render_template("home.html", allposts = placeholder)
    
    return render_template("home.html", allposts = blogPosts)