from flask import Blueprint, render_template, url_for, redirect, Flask
from services.database.database import DataBase
from services.interfaces.ipost_repo import IPostRepo
from services.posts.seed import placeholder
from services.dependency_inject.injector import Services

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("/", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        return render_template("home.html", allposts = posts.get_all())
