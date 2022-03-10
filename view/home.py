from flask import Blueprint, render_template, current_app, url_for, redirect, request
from resources.ipost_repo import IPostRepo
from resources.seed import placeholder
from resources.database_config import DataBaseConfig
from resources.services import Services

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.home = self.bp.route("/", )(self.front_page)

    def goto_db_setup(self):
        if not DataBaseConfig.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        return render_template("home.html", allposts = posts.get_all())
