import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from tests.test_tools import configure, log_user, create_user, create_posts, logout_login

class UsersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    @configure(True)
    def test_create_user(self):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }        
        
        creation = self.test_app.post("/signup", data = user, follow_redirects=True)
        self.assertIn(user["username"], creation.data.decode("UTF-8"))
        self.assertIn(user["email"], creation.data.decode("UTF-8"))
    
    @log_user(2, "John Doe", "JDoe@John", "regular")
    @configure(True)
    def test_delete_user(self):
        read_user = self.test_app.get("view/2/?pg=1")
        self.assertIn("John Doe", read_user.data.decode("UTF-8"))
        result = self.test_app.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
        self.assertEqual("/", urlparse(result.location).path)
        self.assertNotIn("John Doe", result.data.decode("UTF-8"))

    @configure(True)
    def test_create_redirects_to_profile(self):
        user = {
        "username" : "Mark Doe",
        "email" : "MDoe@John",
        "pwd" : "password1@"
        }
        creation = self.test_app.post("/signup", data = user, follow_redirects=False)
        self.assertEqual(urlparse(creation.location).path, url_for("profile.user_profile", user_id = 1))

    @log_user(1, "Mark Doe", "JDoe@John", "regular")
    @configure(True)
    def test_edit_user(self):
        edit = {
        "username" : "James Doe",
        "email" : "MDoe@John",
        "pwd" : "password1@",
        "oldpass" : "password1@"
        }       
        
        self.test_app.post("/edit/1", data = edit, follow_redirects=True)
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn(edit["username"], result.data.decode("UTF-8"))

    @configure(True)
    @log_user(1, "Mark Doe", "JDoe@John", "regular")
    def test_profile_request(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertEqual(result.status_code, 200)

    @configure(True)
    @log_user(1, "Mark Doe", "JDoe@John", "regular")
    def test_read_user(self):
        read_user = self.test_app.get("/view/1/?pg=1")
        self.assertIn("James Doe", read_user.data.decode("UTF-8"))

    @configure(True)
    @log_user(1, "Mark Doe", "JDoe@John", "admin")
    def test_users_show_in_user_listing(self):
        read_users = self.test_app.get("/view/community")
        self.assertIn("James Doe", read_users.data.decode("UTF-8"))

    @configure(True)
    @log_user(1, "Mark Doe", "JDoe@John", "admin")
    def test_deleted_email_in_community(self):
        read_users = self.test_app.get("/view/community")
        self.assertIn("JDoe@John", read_users.data.decode("UTF-8"))

    @configure(False)
    @log_user(1, "Mark Doe", "JDoe@John", "admin")
    def test_redirects_tosetup_if_notConfig(self):
        result = self.test_app.get("/view/1/?pg=1", follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))

if __name__ == "__main__":
    unittest.main()