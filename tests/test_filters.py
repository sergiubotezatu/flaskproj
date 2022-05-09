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
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    users = RepoMngr(IUsersRepo)
    posts = RepoMngr(IPostRepo)

    def create_posts(self, name, count :int, title = "Generic-1"):
        post = {
        "author" : name,
        "title" : title,
        "post" : "This is a test"
        }
        for i in range(0, count):
            post["title"] = post["title"].replace(str(i - 1), str(i))
            self.test_app.post("/post/create", data = post, follow_redirects=False)

    def create_users_with_posts(test_func):
        def decorator(instance):
            users = [("John", "John@mail"), ("Markus", "Mark@mail"), ("James", "James@mail")]
            for user in users:
                instance.users.add(User(user[0], user[1]))
            create = instance.create_posts
            log_user(1, "John", "John@mail", "regular")(create)(instance, "John", 3)
            log_user(2, "Markus", "Mark@mail", "regular")(create)(instance, "Markus", 3)
            log_user(3, "James", "James@mail", "regular")(create)(instance, "James", 3)
            test_func(instance)
            for i in range(1, len(users) + 1):
                instance.users.delete(i)
        return decorator

    @configure(True)
    @create_users_with_posts
    def test_front_pg_displays_all_filterable_users(self):
        self.create_users_with_posts()
        result = self.test_app.get("/")
        self.assertIn('<a href="/?user_id=1&amp;name=John&amp;">John</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=2&amp;name=Markus&amp;">Markus</a>', result.data.decode("UTF-8"))
        self.assertIn('<a href="/?user_id=3&amp;name=James&amp;">James</a>', result.data.decode("UTF-8"))
        

    @configure(True)
    @create_users_with_posts
    def test_front_pg_displays_only_filtered_users_post(self):
        unfiltered_home = self.test_app.get("/")
        self.assertEqual(2, unfiltered_home.data.decode("UTF-8").count("by Markus"))
        filtered = self.test_app.get("/?user_id=1&name=John&")
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by Markus"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by John"))

    @configure(True)
    @create_users_with_posts
    def test_front_pg_displays_multiple_filtered_users(self):
        filtered = self.test_app.get("/?user_id=1&name=John&user_id=3&name=James")
        self.assertEqual(2, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(3, filtered.data.decode("UTF-8").count("by James"))

    @configure(True)
    @create_users_with_posts
    def test_page_change_doesnot_affect_filters(self):
        filtered = self.test_app.get("/?user_id=1&name=John&user_id=3&name=James&pg=2")
        self.assertEqual(1, filtered.data.decode("UTF-8").count("by John"))
        self.assertEqual(0, filtered.data.decode("UTF-8").count("by James"))