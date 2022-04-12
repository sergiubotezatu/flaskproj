from flask import Blueprint, render_template, request, url_for, redirect, Flask
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
        self.filtered = set()
        self.not_filtered = set()
        
    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        rows = len(self.blogPosts)
        posts = None
        filters = request.args.getlist("user_id")
        self.filtered = set()
        if request.method == "POST":
            id = request.form.get("id")
            if id == "x":
                unfilter_id = request.form.get("rmv_id")
                filters.remove(unfilter_id)
            else:
                filters.append(id)
                print(id)
            query_url = ""
            separator = ""
            for filter in filters:
                query_url += f"{separator}{filter}"
                separator = "&user_id="
            route = f"/?user_id={query_url}" if query_url != "" else "/"
            return redirect(route)
        if rows > 0:
            if filters != []:
                posts = self.blogPosts.get_all(filters)
                for post in posts:
                    self.filtered.add((post[1].owner_id, post[1].auth))
                self.not_filtered.difference_update(self.filtered)
            else:
                posts = self.blogPosts.get_all()
                for post in posts:
                    self.not_filtered.add((post[1].owner_id, post[1].auth))
        else:
            posts = placeholder.get_all()
        print(self.not_filtered)
        return render_template("home.html", allposts = posts, filters = self.filtered, users = self.not_filtered)