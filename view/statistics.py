from collections import defaultdict
from datetime import datetime

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
        self.organizer = defaultdict(lambda: 0)
        self.MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    @access.member_required
    def get_statistic(self, user_id):
        user = self.users.get_by(id = user_id)
        self.create_organizer(user)
        return render_template("statistics.html", table = self.organizer, name = user.name)

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def create_organizer(self, user : User):
        start_date = datetime.strptime(user.created, "%d/%b/%y %H:%M:%S").date()
        self.__generate_month_tracker(start_date)
        posts = self.filter.apply({"user_id" : [str(user.id)], "name" : [user.name]}, -1)
        for post in posts:
            date = post[1].created[3:9]
            self.organizer[date] += 1

    def __generate_month_tracker(self, start_date : datetime):
        end_date = datetime.now()
        year_lapse = end_date.year - start_date.year
        month_lapse = year_lapse * 12 + end_date.month - start_date.month
        i = 0
        month_index = start_date.month - 1
        year = int(start_date.year)
        while i <= month_lapse:
            if month_index == 12:
                month_index = 0
                year += 1
            date = self.MONTHS[month_index] + "/" + str(year)[-2:]
            self.organizer[date] = 0
            i += 1
            month_index += 1
        