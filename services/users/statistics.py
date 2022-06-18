from collections import defaultdict

from models.user import User
from services.dependency_inject.injector import Services
from services.interfaces.ifilters import IFilters
from services.interfaces.iuser_statistics import IUserStatistics

class UserStatistics(IUserStatistics):
    @Services.get
    def __init__(self, filter : IFilters):
        self.filter = filter
        
    def get_table(self, user : User):
        table = defaultdict(lambda:0)
        posts = self.filter.apply({"user_id" : [str(user.id)], "name" : [user.name]}, -1)
        for post in posts:
            date = post[1].created[3:9]
            table[date] += 1
        return table
        