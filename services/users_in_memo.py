from services.iusers import IUsers
from services.resources import Services
from services.ipost_repo import IPostRepo
from models.user import User

class Users(IUsers):
    @Services.get
    def __init__(self, posts : IPostRepo):
        self.__users = []
        self.all_posts = posts
        self.deleted = {}
        
    def get_user_by_id(self, id):
        pass

    def check_pass(self, userPass):
        return self.__password == userPass

    def get_posts(self, user_id):
        return self.all_posts.get_user_posts(user_id)

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
        id_names = []
        for users in self.__users:
            id_names.append((users.id, users.name))
        return id_names

    def add_user(self, user : User):
        self.__users.append(user)

    def update_user(self, usr_id, editted, pwd = None):
        for users in self.__users:
            if users.id == usr_id:
                users.edit(editted, pwd)
                break

    def remove_user(self, user: User):
        self.deleted[user.email] = []
        for posts in self.all_posts:
            if user.id == posts.owner_id:
                self.deleted[user.email].append(posts)
        self.__users.remove(user)