from collections import defaultdict
from datetime import datetime

from flask import render_template
from models.post import Post
from services.dependency_inject.injector import Services
from services.interfaces.ifilters import IFilters
from services.interfaces.iusers_repo import IUsersRepo


class UserStatistics:
    @Services.get
    def __init__(self, filter : IFilters, users : IUsersRepo):
        self.filter = filter
        self.users = users
        self.organizer = defaultdict(lambda: 0)
        self.MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def get_statistic(self):
        return render_template("statistics.html", table = self.organizer)

    def get_monthly_count(self, user_id):
        user = self.users.get_by(id = user_id)
        start_date = datetime.strptime(user.created).date()
        self.__generate_organizer(start_date)
        posts = self.filter.apply({"user_id" : user_id}, -1)
        post : Post
        for post in posts:
            date = datetime.strptime(post.created).date()
            self.organizer[date] += 1

    def __generate_organizer(self, start_date : datetime):
        end_date = datetime.now()
        year_lapse = end_date.year - start_date.year
        month_lapse = year_lapse * 12 + end_date.month - start_date.month
        i = 0
        month_index = start_date.month - 1
        year = int(start_date.year)
        while i < month_lapse:
            if month_index == 12:
                month_index = 0
                year += 1
            date = self.MONTHS[month_index] + "/" + str(year)[-2:]
            self.organizer[date] = 0
            i += 1
            month_index += 1
