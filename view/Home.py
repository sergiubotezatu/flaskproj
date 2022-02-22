from flask import Blueprint, render_template, current_app
from services.seed import placeholder

class Home:
    def __init__(self, factory):
        self.blogPosts = factory
        self.bp = self.create_bp()
    
    def create_bp(self):
        home = Blueprint("home", __name__)        
        @home.route("/")
        def front_page():
            rows = len(self.blogPosts)
            if rows == 0:
                return render_template("home.html", allposts = placeholder.get_all())

            return render_template("home.html", allposts = self.blogPosts.get_all())
            
        return home
    