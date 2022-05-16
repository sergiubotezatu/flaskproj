import unittest
from flask import current_app, url_for
from __initblog__ import create_blog
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, create_user, create_posts

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self, *args):
            with self.test_app.session_transaction() as session:
                session["id"] = id
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(*args)
        return wrapper
    return decorator

class FiltersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    users = RepoMngr(IUsersRepo)
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3, "John", 1)
    posts.create_posts_db(3, "Markus", 2)
    posts.create_posts_db(3, "James", 3)
    users.add(User("John", "jodhn@mail"))
    users.add(User("Markus", "markus@mail"))
    users.add(User("James", "james@mail"))
    
    @configure(True)
    def test_front_pg_displays_all_filterable_users(self):
        result = self.test_app.get("/")
        self.assertIn('<a href="/?user_id=1&amp;name=John&amp;">John</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=2&amp;name=Markus&amp;">Markus</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=3&amp;name=James&amp;">James</a>', result.data.decode("UTF-8"))
        

    @configure(True)
    def test_front_pg_displays_only_filtered_users_post(self):
        unfiltered_home = self.test_app.get("/")
        self.assertEqual(2, unfiltered_home.data.decode("UTF-8").count("by Markus"))
        filtered = self.test_app.get("/?user_id=1&name=John&")
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by Markus"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by John"))

    @configure(True)
    def test_front_pg_displays_multiple_filtered_users(self):
        filtered = self.test_app.get("/?user_id=1&name=John&user_id=3&name=James")
        self.assertEqual(2, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by James"))

    @configure(True)
    def test_page_change_doesnot_affect_filters(self):
        filtered = self.test_app.get("/?user_id=1&name=John&user_id=3&name=James&pg=2")
        self.assertEqual(1, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by James"))