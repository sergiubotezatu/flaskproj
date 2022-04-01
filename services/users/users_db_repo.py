from services.dependency_inject.injector import Services
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from models.post import Post
from services.interfaces.idata_base import IDataBase

class UsersDb(IUsersRepo):
    @Services.get
    def __init__(self, db : IDataBase):
        self.db = db
        
    def add_user(self, user : User):
        return self.db.perform("insert_user", user.name, user.email, user.hashed_pass, user.created)[0]        

    def get_posts(self, user_id):
        to_display = self.db.perform("get_user_posts", user_id)
        posts = []
        for post in to_display:
            posts.append((post[0],
            Post(
                post[1],
                post[2],
                self.__cut_poem_newlines(post[3]),
                owner_id = user_id,
                date = post[5]
                ))
                )
        return posts

    def get_user_by(self, **kwargs):
        identifier = ""
        ident_value = None
        if "mail" in kwargs:
            identifier = "get_by_mail"
            ident_value = kwargs["mail"]
        else:
            identifier = "get_by_id"
            ident_value = int(kwargs["id"])
        return self.__get_user(identifier, ident_value)

    def __get_user(self, identifier, value):
        displayed = self.db.perform(identifier, value)
        if displayed == None:
            return displayed
        user = User(displayed[1], displayed[2], displayed[4])
        user.password = displayed[3]
        user.modified = displayed[5]
        user.id = displayed[0]
        return user

    def remove_user(self, user : User):
        self.db.perform("archive", user.id)
        self.db.perform("delete_user", user.id)

    def update_user(self, usr_id, user : User, pwd = ""):
        if pwd != "":
            self.db.perform("change_pass", pwd, usr_id)
        self.db.perform("edit_user", user.name, user.email, user.created, usr_id)

    def get_all(self):
        return self.db.perform("get_users")

    def get_all_inactive(self):
        displayed =  self.db.perform("get_inactive")
        result = []
        for record in displayed:
            result.append((record[0], record[0]))
        return result

    def get_inactive_posts(self, email):
        displayed = self.db.perform("get_removed_posts", email)
        posts = []
        for record in displayed:
            posts.append((email, Post(email, "No title", record[0], owner_id = email)))
        return posts       

    def delete_from_archive(self):
        return self.db.perform("admin_delete")

    def has_account(self, user_id) -> bool:
        return self.db.perform("search", user_id)

    def __cut_poem_newlines(self, content):
        if content == None:
            return ''
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
