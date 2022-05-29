from flask import Blueprint, render_template, request, url_for, redirect, Flask
from services.database.database import DataBase
from services.interfaces.ifilters import IFilters
from services.posts.seed import placeholder
from services.dependency_inject.injector import Services

class Home:
    @Services.get
    def __init__(self, filters : IFilters):
        self.bp = Blueprint("home", __name__)
        self.home = self.bp.route("", methods = ["GET", "POST"])(self.front_page)
        self.to_db_setup = self.bp.before_request(self.setup_first)
        self.filters = filters
        self.PG_LIMIT = 5
        
    def setup_first(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))
        
    def front_page(self):
        page = self.__get_current_page()
        posts = self.filters.apply(request.args.to_dict(flat = False), page)
        if request.method == "POST":
            return redirect(self.filters.get_new_querystr())
        next_page : bool = posts[-1][2] > self.PG_LIMIT
        return render_template("home.html",
                                allposts = posts[0:self.PG_LIMIT],
                                filters = self.filters.filtered_users,
                                users = self.filters.unfiltered_users,
                                next = next_page,
                                pg = int(page),
                                url = request.full_path.replace(f"pg={page}&", ""))

    def __get_current_page(self):
        requested = request.args.get("pg")
        if requested == None:
            return 1
        else:
            return int(requested)