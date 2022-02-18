from flask import Blueprint, render_template, current_app
from services.seed import placeholder
from services.posts_factory import Create

class Home:
    def __init__(self, factory):
        self.blogPosts = factory.create_source()
        self.bp = self.create_bp()
    
    def create_bp(self):
        home = Blueprint("home", __name__)        
        @home.route("/")
        def front_page():
            rows = len(self.blogPosts)
            if rows == 0:
                return render_template("home.html", allposts = placeholder.get_preview())

            return render_template("home.html", allposts = self.blogPosts.get_preview())
        return home
    