import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from services.database.database import DataBase

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

class PaginationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def create_posts(self, name, count :int):
            post = {
            "author" : name,
            "title" : "Generic",
            "post" : "This is a test"
            }
            for i in range(0, count):
                post["title"] = post["title"] + str(i)
                self.test_app.post("/post/create", data = post, follow_redirects=False)
    
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_only_5posts_displayed_on_pg(self):
        self.create_posts("John", 6)
        self.test_app.get(url_for("authentication.log_out"))
        home_pg = self.test_app.get("/")
        something = home_pg.data.decode("UTF-8")
        self.assertEqual(5, home_pg.data.decode("UTF-8").count("John"))
        self.assertIn("Generic4", home_pg.data.decode("UTF-8"))
        self.assertNotIn("Generic5", home_pg.data.decode("UTF-8"))