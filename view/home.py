from flask import Blueprint, render_template, current_app, url_for, redirect, request
from services.seed import placeholder
from services.database import DataBase

class Home:
    def __init__(self, factory):
        self.blogPosts = factory
        self.bp = Blueprint("home", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.home = self.bp.route("/", )(self.front_page)

    def goto_db_setup(self):
        if str(type(self.blogPosts)).find("PostsDb") != -1 and DataBase.config.current_config == None:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        return render_template("home.html", allposts = posts.get_all())
