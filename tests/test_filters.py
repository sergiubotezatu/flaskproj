import unittest
from flask import current_app, url_for
from __initblog__ import create_blog
from tests.test_tools import configure, create_user

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self, *args):
            with self.test_app.session_transaction() as session:
                session["id"] = str(id)
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

    def create_posts(self, name, count :int, title = "Generic-1"):
        post = {
        "author" : name,
        "title" : title,
        "post" : "This is a test"
        }
        for i in range(0, count):
            post["title"] = post["title"].replace(str(i - 1), str(i))
            self.test_app.post("/post/create", data = post, follow_redirects=False)

    @configure(True)
    def test_front_pg_displays_all_filterable_users(self):
        users = [("John", "John@mail"), ("Markus", "Mark@mail"), ("James", "James@mail")]
        for user in users:
            create_user(self, user[0], user[1])
            self.test_app.get(url_for("authentication.log_out"))
        create_posts = self.create_posts
        log_user(1, "John", "John@mail", "regular")(create_posts)(self, "John", 3)
        log_user(2, "Markus", "Mark@mail", "regular")(create_posts)(self, "Markus", 3)
        log_user(3, "James", "James@mail", "regular")(create_posts)(self, "James", 3)
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