import unittest
from flask.testing import FlaskClient
from __initblog__ import create_blog
from services.interfaces.ipost_repo import IPostRepo
from tests.test_helpers import RepoMngr, configure, log_user, create_posts, getClient

class PaginationTests(unittest.TestCase):
    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_available_if_more_posts(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 6)
        home_pg = client.get("/")
        self.assertIn("Next", home_pg.data.decode("UTF-8"))
        self.assertIn("&raquo;", home_pg.data.decode("UTF-8"))
        posts.clear()

    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_next_button_notavailable_if_less_than_6posts(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 5)
        home_pg = client.get("/")
        self.assertNotIn("Next &raquo;", home_pg.data.decode("UTF-8"))
        posts.clear()
    
    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_only_5posts_displayed_on_pg(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 6)
        home_pg = client.get("/")
        self.assertIn("Generic5", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic4", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic3", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic2", home_pg.data.decode("UTF-8"))
        self.assertIn("Generic1", home_pg.data.decode("UTF-8"))
        self.assertNotIn("Generic0", home_pg.data.decode("UTF-8"))
        posts.clear()

    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_button_available_on_second_pg(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 6)
        home_pg = client.get("/?pg=2")
        self.assertIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        posts.clear()

    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_button_notavailable_on_first_pg(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 2)
        home_pg = client.get("/")
        self.assertNotIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        posts.clear()

    @getClient
    @log_user(2, "John", "John@mail", "regular")
    @configure(True)
    def test_previous_and_next_available_middle_pg(self, client : FlaskClient = None):
        posts = RepoMngr(IPostRepo)
        create_posts(client, "John", 11)
        home_pg = client.get("/?pg=2")
        self.assertIn("&laquo; Previous", home_pg.data.decode("UTF-8"))
        self.assertIn("Next", home_pg.data.decode("UTF-8"))
        posts.clear()
