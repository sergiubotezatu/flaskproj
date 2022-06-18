from collections import defaultdict

from flask import Blueprint, render_template
from models.user import User
from services.dependency_inject.injector import Services
from services.interfaces.iauthorization import IAuthorization
from services.interfaces.ifilters import IFilters
from services.interfaces.isession_mngr import ISessionMNGR
from services.interfaces.iusers_repo import IUsersRepo
from services.users.access_decorators import AccessDecorators

class UserStatistics:
    access = AccessDecorators(IAuthorization, ISessionMNGR)

    @Services.get
    def __init__(self, filter : IFilters, users : IUsersRepo):
        self.filter = filter
        self.bp = Blueprint("statistics",  __name__)
        self.get_statistic = self.register("/statistics/<user_id>/", self.get_statistic)
        self.users = users
        self.organizer = defaultdict(lambda:0)

    @access.member_required
    def get_statistic(self, user_id):
        self.organizer = defaultdict(lambda:0)
        user = self.users.get_by(id = user_id)
        self.create_organizer(user)
        return render_template("statistics.html", table = self.organizer, name = user.name)

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def create_organizer(self, user : User):
        posts = self.filter.apply({"user_id" : [str(user.id)], "name" : [user.name]}, -1)
        for post in posts:
            date = post[1].created[3:9]
            self.organizer[date] += 1
        