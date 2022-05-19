import unittest
from flask.testing import FlaskClient
from urllib.parse import urlparse
from __initblog__ import create_blog
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, log_user, getClient

class UsersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)

    users = RepoMngr(IUsersRepo)
    users.add(User("Mark Doe", "Mark@mail"))
    users.add(User("James Doe", "James@mail"))
    users.add(User("Joey Doe", "Joseph@mail"))
    users.add(User("Ross Geller", "Ross@museum"))
    
    @getClient
    @configure(True)
    def test_create_user(self, client : FlaskClient = None):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }        
        
        creation = client.post("/signup", data = user, follow_redirects=True)
        self.assertIn(user["username"], creation.data.decode("UTF-8"))
        self.assertIn(user["email"], creation.data.decode("UTF-8"))
    
    @getClient
    @log_user(2, "James Doe", "James@mail", "regular")
    @configure(True)
    def test_delete_user(self, client : FlaskClient = None):
        profile_pg = client.get("view/2/?pg=1")
        result = client.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
        empty_pg = client.get("view/2/?pg=1")
        self.assertEqual("/", urlparse(result.location).path)
        self.assertIn("James Doe", profile_pg.data.decode("UTF-8"))
        self.assertNotIn("James Doe" ,empty_pg.data.decode("UTF-8"))
    
    @getClient
    @log_user(1, "Mark Doe", "Mark@mail", "regular")
    @configure(True)
    def test_edit_user(self, client : FlaskClient = None):
        edit = {
        "username" : "Markus",
        "email" : "MDoe@John",
        "pwd" : "password1@",
        "oldpass" : ""
        }
        client.post("/edit/1", data = edit, follow_redirects=True)
        result = client.get("/view/1/?pg=1")
        self.assertIn(edit["username"], result.data.decode("UTF-8"))

    @getClient
    @configure(True)
    @log_user(1, "Mark Doe", "Mark@mail", "regular")
    def test_profile_request(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertEqual(result.status_code, 200)

    @getClient
    @configure(True)
    @log_user(1, "Mark Doe", "Mark@mail", "regular")
    def test_read_user(self, client : FlaskClient = None):
        read_user = client.get("/view/1/?pg=1")
        self.assertIn("Mark Doe", read_user.data.decode("UTF-8"))

    @getClient
    @configure(True)
    @log_user(1, "Mark Doe", "MDoe@John", "admin")
    def test_users_show_in_user_listing(self, client : FlaskClient = None):
        read_users = client.get("/view/community")
        self.assertIn("Joey Doe", read_users.data.decode("UTF-8"))

    @getClient
    @configure(True)
    @log_user(1, "Mark Doe", "MDoe@John", "admin")
    def test_deleted_show_in_user_listing(self, client : FlaskClient = None):
        self.users.delete(4)
        read_users = client.get("/view/community")
        self.assertIn("Ross@museum", read_users.data.decode("UTF-8"))

    @getClient
    @configure(False)
    @log_user(1, "Mark Doe", "MDoe@John", "admin")
    def test_redirects_tosetup_if_notConfig(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1", follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))

if __name__ == "__main__":
    unittest.main()