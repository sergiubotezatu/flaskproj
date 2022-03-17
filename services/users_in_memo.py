from services.iusers import IUsers
from services.resources import Services
from services.ipost_repo import IPostRepo
from models.user import User

class Users(IUsers):
    @Services.get
    def __init__(self, posts : IPostRepo):
        self.__users = []
        self.all_posts = posts
        
    def get_user_by_id(self, id):
        pass

    def check_pass(self, userPass):
        return self.__password == userPass

    def get_posts(self, user_name):
        return self.all_posts.get_user_posts(user_name)

    def get_user_by_mail(self, mail) -> User:
        for users in self.__users:
            if mail == users.email:
                return users
        return None

    def get_user_by_id(self, id : int) -> User:
        for users in self.__users:
            if id == users.id:
                return users
        return None

    def get_all(self):
        names = []
        for users in self.__users:
            names.append(users.name)
        return names

    def add_user(self, user : User):
        self.__users.append(user)