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
        self.count = 0
        
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
        self.count += 1
        user.id = self.count
        self.__users.append(user)
        
    def update_user(self, usr_id, editted, pwd = None):
        for users in self.__users:
            if users.id == usr_id:
                if users.name != editted.name:
                    self.all_posts.reflect_user_changes(usr_id, editted.name)
                self.__change_user_info(users, editted, pwd)
                break

    def __change_user_info(user, new_user, pwd):
        user.name = new_user.name
        user.email = new_user.email
        user.modified = new_user.created
        if pwd != None: 
            user.password = pwd
    
    def remove_user(self, user: User):
        self.deleted[user.email] = []
        for posts in self.all_posts:
            if user.id == posts.owner_id:
                self.deleted[user.email].append(posts)
        self.__users.remove(user)

    def has_account(self, user_id) -> bool:
        for user in self.__users:
            if user.id == user_id:
                return True
                break
        return False
