from services.interfaces.iusers_repo import IUsersRepo
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo
from models.user import User
from models.post import Preview

class Users(IUsersRepo):
    @Services.get
    def __init__(self, posts : IPostRepo):
        self.__users = []
        self.all_posts : IPostRepo = posts
        self.deleted = {}
        self.count = 0
        
    def get_posts(self, user_id):
        user_posts = []
        for posts in self.all_posts:
            if posts[1].owner_id == user_id:
                user_posts.append((posts[0], Preview(posts[1])))
        return user_posts  
        

    def get_user_by(self, **kwargs):
        match = self.same_id if "id" in kwargs else self.same_mail
        identifier = kwargs["id"] if "id" in kwargs else kwargs["mail"]
        for user in self.__users:
            if match(user, identifier):
                return user
        return None

    def same_id(self, user : User, id):
        return user.id == id

    def same_mail(user : User, mail):
        return user.email == mail

    def get_all(self):
        id_names = []
        for users in self.__users:
            id_names.append((users.id, users.name))
        return id_names

    def add_user(self, user : User):
        self.count += 1
        user.id = self.count
        self.__users.append(user)
        return user.id
        
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
