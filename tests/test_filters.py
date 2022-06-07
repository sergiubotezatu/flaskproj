import unittest
from flask.testing import FlaskClient
from __initblog__ import create_blog
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, getClient

class FiltersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False) 
    users = RepoMngr(IUsersRepo)
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3, "John", 1)
    posts.create_posts_db(3, "Markus", 2)
    posts.create_posts_db(3, "James", 3)
    users.add(User("John", "jodhn@mail"))
    users.add(User("Markus", "markus@mail"))
    users.add(User("James", "james@mail"))
    
    @getClient
    @configure(True)
    def test_front_pg_displays_all_filterable_users(self, client : FlaskClient = None):
        result = client.get("/")
        self.assertIn('<a href="/?user_id=1&amp;name=John&amp;">John</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=2&amp;name=Markus&amp;">Markus</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=3&amp;name=James&amp;">James</a>', result.data.decode("UTF-8"))        

    @getClient
    @configure(True)
    def test_front_pg_displays_only_filtered_users_post(self, client : FlaskClient = None):
        unfiltered_home = client.get("/")
        self.assertEqual(2, unfiltered_home.data.decode("UTF-8").count("by Markus"))
        filtered = client.get("/?user_id=1&name=John&")
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by Markus"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by John"))

    @getClient
    @configure(True)
    def test_front_pg_displays_multiple_filtered_users(self, client : FlaskClient = None):
        filtered = client.get("/?user_id=1&name=John&user_id=3&name=James")
        self.assertEqual(2, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by James"))

    @getClient
    @configure(True)
    def test_page_change_doesnot_affect_filters(self, client : FlaskClient = None):
        filtered = client.get("/?user_id=1&name=John&user_id=3&name=James&pg=2")
        self.assertEqual(1, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by James"))