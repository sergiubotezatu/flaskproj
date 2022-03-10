from flask import Blueprint, render_template, current_app, url_for, redirect, request
from services.ipost_repo import IPostRepo
from services.seed import placeholder
from services.database import DataBase
from services.services import Services

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.home = self.bp.route("/", )(self.front_page)

    def goto_db_setup(self):
        if not DataBase.config.isConfigured():
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        for x in posts:
            print(x)
        return render_template("home.html", allposts = posts.get_all())
