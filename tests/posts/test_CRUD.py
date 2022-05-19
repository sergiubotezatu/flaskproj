import unittest
from flask.testing import FlaskClient
from urllib.parse import urlparse
from __initblog__ import create_blog
from services.interfaces.ipost_repo import IPostRepo
from tests.test_helpers import RepoMngr, log_user, configure, getClient

class PostsTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)
        
    BASE =  "/"
    BASE_POST = "/post/"
    CONFIG_PAGE = "/config"
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3)

    @getClient
    @configure(True)
    def test_setuppage_redirects_if_configured(self, client : FlaskClient = None):
        result = client.get(self.CONFIG_PAGE, follow_redirects = False)
        self.assertEqual(result.status_code, 302)
    
    @getClient
    @configure(False)
    def test_setuppage_doesnt_redirect_if_notconfig(self, client : FlaskClient = None):
        result = client.get(self.CONFIG_PAGE, follow_redirects = False)
        self.assertEqual(result.status_code, 200)
    
    @getClient
    @configure(False)
    def test_home_redirects_tosetup_if_notConfig(self, client : FlaskClient = None):
        result = client.get(self.BASE, follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))
        
    @getClient
    @log_user(3, "Mark Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_create_redirect(self, client : FlaskClient = None):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }
        result = client.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        self.assertEqual(result.status_code, 302)
    
    @getClient
    @log_user(3, "Mark Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_create_post(self, client : FlaskClient = None):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }        
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.assertIn(post["title"], creation.data.decode("UTF-8"))
        self.assertIn(post["post"], creation.data.decode("UTF-8"))        

    @getClient
    @log_user(3, "James Doe", "Mark@email.com", "regular")   
    @configure(True)
    def test_creation_home_print(self, client : FlaskClient = None):
        post = {
        "author" : "James Doe",
        "title" : "Generic",
        "post" : "I am printed on home page."
        }
        client.post(self.BASE_POST + "create", data = post)
        result = client.get(self.BASE)
        self.assertIn(post["post"], result.data.decode("UTF-8"))

    @getClient
    @log_user(2, "John Doe", "Mark@email.com", "regular")
    @configure(True)
    def test_edit_post(self, client : FlaskClient = None):
        edit = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "This is an edit"
        }
        initial = client.get(self.BASE_POST + "read/3/")
        self.assertIn("Test post 3", initial.data.decode("UTF-8"))
        client.post(self.BASE_POST + "edit/3", data = edit, follow_redirects=True)
        result = client.get(self.BASE_POST + "read/3/")
        self.assertIn(edit["post"], result.data.decode("UTF-8"))

    @getClient
    @log_user(2, "John Doe", "JDoe@email.com", "regular")
    @configure(True)
    def test_delete_post(self, client : FlaskClient = None):
        post = {
        "author" : "John Doe",
        "title" : "Generic",
        "post" : "Test post 1"
        }
        read = client.get(self.BASE_POST + "read/1/")
        self.assertIn(post["author"], read.data.decode("UTF-8"))
        self.assertIn(post["title"], read.data.decode("UTF-8"))
        self.assertIn(post["post"], read.data.decode("UTF-8"))
        result = client.post(self.BASE_POST + "read/1", data = {"postID" : "1"})
        self.assertNotIn(post["author"], result.data.decode("UTF-8"))

    @getClient
    @log_user(2, "John Doe", "Generic", "regular")
    @configure(True)
    def test_redirect_delete(self, client : FlaskClient = None):
        result = client.post(
            self.BASE_POST + "read/2/",
            data = {"postID" : "2"},
            follow_redirects=False)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(urlparse(result.location).path, "/")
        
if __name__ == "__main__":
    unittest.main()