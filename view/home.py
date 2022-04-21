from collections import defaultdict
from flask import Blueprint, render_template, request, url_for, redirect, Flask
from services.database.database import DataBase
from services.interfaces.ipost_repo import IPostRepo
from services.posts.seed import placeholder
from services.dependency_inject.injector import Services
from urllib.parse import urlencode

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("/", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.not_filtered = self.get_not_filtered_users()
        self.PG_LIMIT = 5
        
    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
    
    def front_page(self):
        filters = defaultdict(lambda: [], request.args.to_dict(flat = False))
        rows = len(self.blogPosts)
        posts = None
        page = filters["pg"]
        if len(page) == 0:
                page = 1
        else:
            page = int(page[0])
        if rows > 0 :
            filtered_ids = filters["user_id"]
            filtered_names = filters["name"]
            self.__update_not_filtered(filtered_ids, filtered_names)
            posts = self.blogPosts.get_all(page, filtered_ids)
        else:
            posts = placeholder.get_all()
        if request.method == "POST":
            return self.__remove_filters()
        next_page : bool = posts[-1][2] > self.PG_LIMIT
        return render_template("home.html",
        allposts = posts[0:self.PG_LIMIT],
        filters = filters,
        users = self.not_filtered,
        next = next_page,
        pg = int(page),
        url = request.full_path.replace(f"pg={page}&", ""))

    def get_not_filtered_users(self) -> set:
        result = set()
        if len(self.blogPosts) > 0:
            for post in self.blogPosts.get_all(pagination = False):
                result.add((str(post[1].owner_id), post[1].auth))
        return result

    def __remove_filters(self):
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        return redirect(query_url)

    def __update_not_filtered(self, ids, names):
        if ids == []:
            self.not_filtered = self.get_not_filtered_users()
        for i in range(0, len(ids)):
            self.not_filtered.discard((ids[i], names[i]))