from collections import defaultdict
from models.user import User
from models.stats_model import StatisticsModel
from services.dependency_inject.injector import Services
from services.interfaces.ifilters import IFilters
from services.interfaces.iuser_statistics import IUserStatistics
from services.interfaces.iusers_repo import IUsersRepo

class UserStatistics(IUserStatistics):
    @Services.get
    def __init__(self, filter : IFilters, users : IUsersRepo):
        self.filter = filter
        self.users = users
        
    def get(self, id) -> StatisticsModel:
        user = self.users.get_by(id = id)
        name = user.name
        monthly_posts_count : defaultdict[str , int] = defaultdict(lambda:0)
        posts = self.filter.apply({"user_id" : [str(id)], "name" : [name]}, -1)
        for post in posts:
            date = post[1].created[3:9]
            monthly_posts_count[date] += 1
        if len(monthly_posts_count) == 0:
            monthly_posts_count["N/A"] = f"{name} has no posting activity."
        return StatisticsModel(name, monthly_posts_count)
        