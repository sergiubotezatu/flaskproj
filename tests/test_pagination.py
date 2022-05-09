import unittest
from flask import current_app
from __initblog__ import create_blog
from services.database.database import DataBase
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, log_user, create_posts

class PaginationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()
    
    posts = RepoMngr(IPostRepo)

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_available_if_more_posts(self):
        create_posts(self, "John", 6)
        home_pg = self.test_app.get("/")
        self.assertIn("Next", home_pg.data.decode("UTF-8"))
        self.assertIn("&raquo;", home_pg.data.decode("UTF-8"))
        for i in range (0, 6):
            self.posts.delete(i + 1)

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_notavailable_if_less_than_6posts(self):
        create_posts(self, "John", 5)
        home_pg = self.test_app.get("/")
        self.assertNotIn("Next &raquo;", home_pg.data.decode("UTF-8"))
        for i in range (0, 5):
            self.posts.delete(i + 1)
    
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_only_5posts_displayed_on_pg(self):
        create_posts(self, "John", 6)
        home_pg = self.test_app.get("/")
        self.assertIn("Generic5", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic4", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic3", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic2", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic1", home_pg.data.decode("UTF-8"))
        self.assertNotIn("Generic0", home_pg.data.decode("UTF-8"))
        for i in range (0, 6):
            self.posts.delete(i + 1)

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_button_available_on_second_pg(self):
        create_posts(self, "John", 6)
        home_pg = self.test_app.get("/?pg=2")
        self.assertIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        for i in range (0, 6):
            self.posts.delete(i + 1)

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_button_notavailable_on_first_pg(self):
        create_posts(self, "John", 2)
        home_pg = self.test_app.get("/")
        self.assertNotIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        for i in range (0, 2):
            self.posts.delete(i + 1)

    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_and_next_available_middle_pg(self):
        create_posts(self, "John", 11)
        home_pg = self.test_app.get("/?pg=2")
        self.assertIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        self.assertIn("Next", home_pg.data.decode("UTF-8"))
        for i in range (0, 11):
            self.posts.delete(i + 1)
