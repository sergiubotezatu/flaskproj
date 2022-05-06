from unittest import TestCase
from flask import url_for
from models.post import Post
from services.database.database import DataBase
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo

def delete_post(posts : IPostRepo, id : int):
    posts.remove(id)

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(instance : TestCase):
            with instance.test_app.session_transaction() as session:
                session["id"] = str(id)
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