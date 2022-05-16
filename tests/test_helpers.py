from typing import Union
from unittest import TestCase
from flask import url_for
from models.post import Post
from models.user import User
from services.database.database import DataBase
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo

class RepoMngr:
    first_instance = True
    @Services.get
    def __init__(self, repo : Union[IPostRepo, IUsersRepo]):
        self.repo = repo
        self.__del_placeholder()

    def create_posts_db(self, count : int, name = "John Doe", owner_id = 2):
        for i in range(count):
            post = Post(name, "Generic", f"Test post {str(i + 1)}", owner_id)
            self.repo.add(post)
        
    def delete(self, id = 0):
        self.repo.remove(id)

    def add(self, entity : Union[Post, User]):
        self.repo.add(entity)

    def add_rmv(self, entity : Union[Post, User]):
        def decorator(test_func):
            def wrapper(instance):
                self.add(entity)
                test_func(instance)
                self.delete(id = entity.id)
            return wrapper
        return decorator

    def __del_placeholder(self):
        if RepoMngr.first_instance and "Posts" in str(type(self.repo)):
            RepoMngr.first_instance = False
            self.delete(1)

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(instance : TestCase):
            with instance.test_app.session_transaction() as session:
                session["id"] = id
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(instance)
        return wrapper
    return decorator

def configure(is_config : bool):
    def decorator(test_func):
        def wrapper(instance):
            DataBase.config.is_configured = is_config
            return test_func(instance)
        return wrapper
    return decorator

def create_user(instance : TestCase, name, email):
        user = {
                "username" : name,
                "email" : email,
                "pwd" : "password1@"
                }
        instance.test_app.post("/signup", data = user, follow_redirects=False)

def create_posts(instance : TestCase, name, count :int, title = "Generic-1"):
        post = {
        "author" : name,
        "title" : title,
        "post" : "This is a test"
        }
        for i in range(0, count):
            post["title"] = post["title"].replace(str(i - 1), str(i))
            instance.test_app.post("/post/create", data = post, follow_redirects=False)

def logout_login(instance : TestCase, mail):
        user = {
            "email" : mail,
            "pwd" : "password1@"
        }
        instance.test_app.get(url_for("authentication.log_out"))
        instance.test_app.post("/login", data = user, follow_redirects=False)