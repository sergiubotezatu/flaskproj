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

    def create_posts(self, name, count :int, title = "Generic-1"):
            post = {
            "author" : name,
            "title" : title,
            "post" : "This is a test"
            }
            for i in range(0, count):
                post["title"] = post["title"].replace(str(i - 1), str(i))
                self.test_app.post("/post/create", data = post, follow_redirects=False)
        
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_available_if_more_posts(self):
        self.create_posts("John", 6)
        home_pg = self.test_app.get("/")
        self.assertIn("Next &raquo;", home_pg.data.decode("UTF-8"))

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_notavailable_if_less_than_6posts(self):
        self.test_app.post("/post/read/1", data = {"postID" : "1"})
        self.test_app.post("/post/read/2", data = {"postID" : "2"})
        home_pg = self.test_app.get("/")
        self.assertNotIn("Next &raquo;", home_pg.data.decode("UTF-8"))
    
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_only_5posts_displayed_on_pg(self):
        self.create_posts("John", 1, title = "Generic1")
        home_pg = self.test_app.get("/")
        self.assertIn("Generic5", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic4", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic3", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic2", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic1", home_pg.data.decode("UTF-8"))
        self.assertNotIn("Generic0", home_pg.data.decode("UTF-8"))

    @configure(True)
    def test_previous_button_available_on_second_pg(self):
        home_pg = self.test_app.get("/?pg=2")
        self.assertIn("&laquo; Previous", home_pg.data.decode("UTF-8"))

    @configure(True)
    def test_previous_button_notavailable_on_first_pg(self):
        home_pg = self.test_app.get("/")
        self.assertNotIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
