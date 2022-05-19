import unittest
from flask.testing import FlaskClient
from __initblog__ import create_blog
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, getClient, log_user

class AuthorizationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)

    users = RepoMngr(IUsersRepo)
    users.add(User("Mark", "Mark@mail"))
    
    @getClient
    @log_user(3, "Admin", "admin@admin", "admin")
    @configure(True)
    def test_admins_can_edit_others(self, client : FlaskClient = None):
        result = client.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))
        self.assertIn("Select new role for the user", result.data.decode("UTF-8"))
        
    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_user_listing_allowed_for_admins(self, client : FlaskClient = None):
        result = client.get("/view/community")
        self.assertNotIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertNotIn("only admins have access", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_user_listing_raises_403error_if_not_admin(self, client : FlaskClient = None):
        result = client.get("/view/community")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("only admins have access", result.data.decode("UTF-8"))

    @getClient
    @log_user(3, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_edit_delete_button_allowed_for_admins(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "Mark", "Mark@mail", "regular")
    @configure(True)
    def test_edit_delete_button_allowed_for_owners(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @getClient
    @log_user(2, "John Doe", "JDoe@mail", "regular")
    def test_edit_delete_button_notallowed_for_others(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertNotIn("Edit info", result.data.decode("UTF-8"))
        self.assertNotIn("Delete account", result.data.decode("UTF-8"))

    @getClient
    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others(self, client : FlaskClient = None):
        result = client.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "Mark", "Mark@mail", "regular")
    @configure(True)
    def test_members_can_edit_themselves(self, client : FlaskClient = None):
        result = client.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))

    @getClient
    @configure(True)
    def test_not_members_cannot_edit_users(self, client : FlaskClient = None):
        result = client.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_profile_allowed_for_members(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("John Doe", result.data.decode("UTF-8"))

    @getClient
    @configure(True)
    def test_profile_path_raises_403error_if_not_member(self, client : FlaskClient = None):
        result = client.get("/view/1/?pg=1")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_users_creation_allowed_for_admins(self, client : FlaskClient = None):
        result = client.get("/create")
        self.assertIn("What type of user are you creating", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_users_creation_not_allowed_for_others(self, client : FlaskClient = None):
        result = client.get("/create")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("only admins have access", result.data.decode("UTF-8"))

    
        