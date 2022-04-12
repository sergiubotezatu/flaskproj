from flask import Blueprint, render_template, request, url_for, redirect, Flask
from services.database.database import DataBase
from services.interfaces.ipost_repo import IPostRepo
from services.posts.seed import placeholder
from services.dependency_inject.injector import Services

class Home:
    i = 0
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("/", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.posting_users = []
        self.filters = []
        
    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        id = None
        if request.method == "POST":
            id = request.form.get("user")
            name = request.form.get("name")
            if id != "x":
                self.filters.append((id, name))
                self.posting_users.remove((int(id), name))
                query_url = "?"
                i = 0
                for filter in self.filters:
                    query_url += f"usr_id{i}={filter[0]}&"
                return redirect(f"/{query_url}")
            else:
                usr_id = request.form.get("id")
                self.filters.remove((usr_id, name))
                self.posting_users.append((int(usr_id), name))
            return render_template("home.html", filters = self.filters, users = self.posting_users, allposts = self.blogPosts.get_all())
        rows = len(self.blogPosts)
        posts = None
        if rows > 0:
            posts = self.blogPosts
            self.posting_users = self.blogPosts.get_with_posts()
            getter = posts.get_user_posts(id) if id != None else posts.get_all()
        else:
            posts = placeholder
        return render_template("home.html", filters = self.filters, users = self.posting_users, allposts = getter)
