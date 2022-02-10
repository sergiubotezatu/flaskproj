import unittest
from flask import url_for, current_app
from __init__ import create_blog

class BlogTests(unittest.TestCase):
    def setUp(self):
        self.blog = create_blog()
        self.blog.config["testing"] = True
        with self.blog.app_context():
            self.test_app = current_app.test_client()

    BASE =  "http://127.0.0.1:5000/"
    BASE_POST = "http://127.0.0.1:5000/post/"

    def test_home(self):
        result = self.test_app.get(self.BASE)
        self.assertEqual(result.status_code, 200)

    def test_create_request(self):
        result = self.test_app.get(self.BASE_POST + "create")
        self.assertEqual(result.status_code, 200)

    def test_create_newpost(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        result = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        with self.blog.test_request_context():
            self.assertEqual(result.location.replace("127.0.0.1:5000", "localhost"),
             url_for("posts.read", post_id = "Jo1", _external = True))
    
    def test_read_post(self):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }
        creation = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        result = self.test_app.get(self.BASE_POST + "read/post_id_Jo1")
        self.assertEqual(result.get_json(), post)

    if __name__ == "__main__":
        unittest.main()
