from flask import Blueprint, render_template, current_app, url_for, redirect, request, session, flash
from services.ipost_repo import IPostRepo
from services.seed import placeholder
from services.resources import Services
from services.database import DataBase
from view.user_profile import Session

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.home = self.bp.route("/", methods = ["GET", "POST"])(self.front_page)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        if request.method == "POST":
            Session.empty()
            flash(f"You have been logged out. See you again soon!")
        rows = len(self.blogPosts)
        posts = self.blogPosts if rows > 0 else placeholder
        return render_template("home.html", allposts = posts.get_all())
