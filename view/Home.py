from flask import Blueprint, render_template, current_app, url_for, redirect, request
from services.seed import placeholder

class Home:
    def __init__(self, factory):
        self.blogPosts = factory
        self.bp = Blueprint("home", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.home = self.bp.route("/")(self.front_page)

    def goto_db_setup(self):
        if str(type(self.blogPosts)).find("PostsDb") != -1 and self.blogPosts.db.current_config == None:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        if rows == 0:
            return render_template("home.html", allposts = placeholder.get_all())

        return render_template("home.html", allposts = self.blogPosts.get_all())
