import unittest
from urllib.parse import urlparse
from flask import  current_app
from __initblog__ import create_blog
from services.database.database import DataBase
from tests.test_tools import log_user, configure

class PostsTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()
        
    BASE =  "/"
    BASE_POST = "/post/"
    CONFIG_PAGE = "/config"    

    @configure(True)
    def test_setuppage_redirects_if_configured(self):
        result = self.test_app.get(self.CONFIG_PAGE, follow_redirects = False)
        self.assertEqual(result.status_code, 302)
        
    @configure(False)
    def test_setuppage_doesnt_redirect_if_notconfig(self):
        result = self.test_app.get(self.CONFIG_PAGE, follow_redirects = False)
        self.assertEqual(result.status_code, 200)
        
    @configure(False)
    def test_home_redirects_tosetup_if_notConfig(self):
        result = self.test_app.get(self.BASE, follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))
        
    @configure(True)
    def test_create_home_request(self):
        result = self.test_app.get(self.BASE)
        self.assertEqual(result.status_code, 200)
        
    @log_user(2, "Mark Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_create_redirect(self):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        result = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(urlparse(result.location).path, "/post/read/3")
    
    @log_user(2, "Mark Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_create_post(self):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }
        
        creation = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.assertIn(post["title"], creation.data.decode("UTF-8"))
        self.assertIn(post["post"], creation.data.decode("UTF-8"))
        
    @configure(True)
    def test_creation_home_print(self):
        post = {
        "author" : "James Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }

        self.test_app.post(self.BASE_POST + "create", data = post)
        result = self.test_app.get(self.BASE)
        self.assertIn(post["post"], result.data.decode("UTF-8"))

    @log_user(2, "Mark Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_edit_post(self):
        edit = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is an edit"
        }

        self.test_app.post(self.BASE_POST + "edit/2", data = edit, follow_redirects=True)
        result = self.test_app.get(self.BASE_POST + "read/2")
        self.assertIn(edit["post"], result.data.decode("UTF-8"))

    @log_user(1, "Greg Doe", "Greg@email.com", "regular")
    @configure(True)
    def test_delete_post(self):
        post = {
        "author" : "Greg Doe",
        "title" : "Generic",
        "post" : "This is a delete test"
        }

        creation = self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.assertIn(post["author"], creation.data.decode("UTF-8"))
        self.assertIn(post["title"], creation.data.decode("UTF-8"))
        self.assertIn(post["post"], creation.data.decode("UTF-8"))
        result = self.test_app.post(self.BASE_POST + "read/4", data = {"postID" : "4"})
        self.assertNotIn(post["author"], result.data.decode("UTF-8"))

    @log_user(1, "Greg Doe", "Greg@email.com", "regular")
    @configure(True)
    def test_redirect_delete(self):
        post = {
        "author" : "Greg Doe",
        "title" : "Generic",
        "post" : "This is a delete test"
        }

        self.test_app.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        result = self.test_app.post(
            self.BASE_POST + "read/4",
            data = {"postID" : "4"},
            follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(urlparse(result.location).path, "/")
        
if __name__ == "__main__":
    unittest.main()