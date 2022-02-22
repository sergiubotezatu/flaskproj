from flask import Blueprint, render_template, current_app, url_for, redirect, request
from services.seed import placeholder

class Home:
    def __init__(self, factory):
        self.blogPosts = factory
        self.bp = self.create_bp()
    
    def create_bp(self):
        home = Blueprint("home", __name__)

        @home.before_request
        def goto_db_setup():
            if str(type(self.blogPosts)).find("PostsDb") != -1 and self.blogPosts.db.current_config == None:
                return redirect(url_for("db_setup.set_database"))
        
        @home.route("/")
        def front_page():
            rows = len(self.blogPosts)
            if rows == 0:
                return render_template("home.html", allposts = placeholder.get_all())

            return render_template("home.html", allposts = self.blogPosts.get_all())

        return home
    