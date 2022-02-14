import unittest
from flask import url_for, current_app
from __init__ import create_blog
from postRepo.seed import blogPosts


class BlogTests(unittest.TestCase):
    def setUp(self):
        self.blog = create_blog()
        self.blog.config["TESTING"] = True
        self.blog.secret_key = "FlaskBlog"
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def tearDown(self) -> None:
        blogPosts.delete_all()

    BASE =  "/"
    BASE_POST = "/post/"

    def test_home(self):
        result = self.test_app.get(self.BASE)
        self.assertEqual(result.status_code, 200)

    def test_create_request(self):
        result = self.test_app.get(self.BASE_POST + "create")
        self.assertEqual(result.status_code, 200)

    def test_create_redirect(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        result = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.location.replace("127.0.0.1:5000", "localhost"),
        url_for("posts.read", post_id = "Jo1", _external = True))
    
    def test_create_post(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        creation = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.assertIn(post["author"], creation.data.decode("UTF-8"))
        self.assertIn(post["title"], creation.data.decode("UTF-8"))
        self.assertIn(post["post"], creation.data.decode("UTF-8"))

    def test_creation_home_print(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        self.test_app.post(self.BASE_POST + "create", data = post)
        result = self.test_app.get(self.BASE)
        self.assertIn(post["post"], result.data.decode("UTF-8"))

    def test_edit_request(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        edit = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is an edit"
        }

        self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.test_app.post(self.BASE_POST + "edit/Jo1", data = edit, follow_redirects=True)
        result = self.test_app.get(self.BASE_POST + "read/Jo1")
        self.assertIn(edit["post"], result.data.decode("UTF-8"))

    def test_delete_post(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a delete test"
        }

        self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        result = self.test_app.post(self.BASE_POST + "read/Jo1", data = {"postID" : "Jo1"})
        self.assertNotIn(post["post"], result.data.decode("UTF-8"))

    def test_redirect_delete(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a delete test"
        }

        self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        result = self.test_app.post(
            self.BASE_POST + "read/Jo1",
            data = {"postID" : "Jo1"},
            follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.location.replace("127.0.0.1:5000", "localhost"),
        url_for("home.front_page", _external = True))
   
    if __name__ == "__main__":
        unittest.main()