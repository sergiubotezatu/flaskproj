import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.database.database import DataBase
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self):
            with self.test_app.session_transaction() as session:
                session["id"] = str(id)
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(self)
        return wrapper
    return decorator

def configure(is_config : bool):
    def decorator(test_func):
        def wrapper(self):
            DataBase.config.is_configured = is_config
            return test_func(self)
        return wrapper
    return decorator

class PostsUsersLinkTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def create_user(self, name, mail):
        user = {
                "username" : name,
                "email" : mail,
                "pwd" : "password1@"
                }
        self.test_app.post("/signup", data = user, follow_redirects=False)

    def create_posts(self, name, count :int):
        post = {
        "author" : name,
        "title" : "Generic",
        "post" : "This is a test"
        }
        for i in range(0, count):
            post["title"] = post["title"] + str(i)
            self.test_app.post("/post/create", data = post, follow_redirects=False)

    @Services.get
    def get_posts(self, posts : IPostRepo):
        return posts
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_ownerId_from_user(self):
        self.create_posts("John", 3)
        posts = self.get_posts(IPostRepo).get_all()
        for post in posts:
            if post[0] != "Ch1":
                self.assertEqual("2", post[1].owner_id)
