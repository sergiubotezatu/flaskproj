from flask import Blueprint, render_template, url_for, redirect, Flask
from services.ipost_repo import IPostRepo
from services.seed import placeholder
from services.resources import Services
from services.access_decorators import decorator

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("/", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)

    @decorator.only_once
    def goto_db_setup(self):
        return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        return render_template("home.html", allposts = posts.get_all())
