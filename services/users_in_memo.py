from services.iusers import IUsers
from services.resources import Services
from services.ipost_repo import IPostRepo
from models.user import User

class Users(IUsers):
    @Services.get
    def __init__(self, posts : IPostRepo):
        self.__users = []
        self.all_posts = posts
        self.id = 1
    
    def get_user_by_id(self, id):
        pass

    def check_pass(self, userPass):
        return self.__password == userPass

    def get_posts(self, user_name):
        return self.all_posts.get_user_posts(user_name)

    def get_user_by_name(self, username) -> User:
        for users in self.__users:
            if username == users.name:
                return users
        return None

    def add_user(self, user : User):
        self.__users.append(user)