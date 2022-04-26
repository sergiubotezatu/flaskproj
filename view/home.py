from flask import Blueprint, render_template, request, url_for, redirect, Flask
from services.database.database import DataBase
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo
from services.posts.filters import Filters
from services.posts.seed import placeholder
from services.dependency_inject.injector import Services

class Home:
    @Services.get
    def __init__(self, repo : IPostRepo, filter : IFilters):
        self.blogPosts = repo
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.setup_first)
        self.filter = filter
        self.PG_LIMIT = 5
        
    def setup_first(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
        self.filter.set_not_filtered(self.blogPosts)
    
    def front_page(self):
        page = self.__get_current_page()
        posts = self.__get_displayed_posts(page)
        if request.method == "POST":
            return redirect(self.filter.get_new_path())
        next_page : bool = posts[-1][2] > self.PG_LIMIT

        return render_template("home.html",
        allposts = posts[0:self.PG_LIMIT],
        filters = self.filter.filters,
        users = self.filter.not_filtered,
        next = next_page,
        pg = int(page),
        url = request.full_path.replace(f"pg={page}&", ""))

    def __get_displayed_posts(self, page):
        if len(self.blogPosts) > 0 :
            self.filter.set_current_filters()
            self.filter.update_not_filtered(self.blogPosts)
            return self.blogPosts.get_all(page, self.filter.ids)
        else:
            return placeholder.get_all()

    def __get_current_page(self):
        requested = request.args.get("pg")
        if requested == None:
            return 1
        else:
            return int(requested)