import unittest
from urllib.parse import urlparse
from flask import current_app
from __initblog__ import create_blog
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
    def test_posts_get_ownerId_from_logged_user(self):
        self.create_posts("John", 3)
        posts = self.get_posts(IPostRepo).get_all()
        for post in posts:
            if post[1].auth == "John":
                self.assertEqual("2", post[1].owner_id)
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_name_from_logged_user(self):
        result = self.test_app.get("/post/create")
        self.assertIn("John Doe", result.data.decode("UTF-8"))

    @configure(True)
    def test_editting_ownerId_reflects_in_posts(self):
        self.create_user("Mark Doe", "JDoe@John")
        self.create_posts("Mark Doe", 1)
        edit = {
        "username" : "James Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@",
        "oldpass" : "password1@"
        }
        self.test_app.post("/edit/1", data = edit, follow_redirects=True)
        posts = self.get_posts(IPostRepo).get_all()
        for post in posts:
            if post[1].owner_id == "2":
                self.assertEqual("James Doe", posts[1].auth)

    @configure(True)
    def test_deleting_user_deletes_owned_posts(self):
        self.test_app.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
        posts = self.get_posts(IPostRepo)
        for post in posts:
            self.assertNotEqual("James", post.auth)
