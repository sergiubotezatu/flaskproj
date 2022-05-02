import unittest
from flask import current_app
from __initblog__ import create_blog
from services.database.database import DataBase
from tests.test_tools import configure, log_user, create_posts

class PaginationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_available_if_more_posts(self):
        create_posts(self, "John", 6)
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
        create_posts(self, "John", 1, title = "Generic1")
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
