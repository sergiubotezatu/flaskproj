import unittest
from flask import current_app, url_for
from __initblog__ import create_blog
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, log_user, create_user, create_posts, logout_login

class AuthorizationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    users = RepoMngr(IUsersRepo)
    
    @log_user(3, "Admin", "admin@admin", "admin")
    @configure(True)
    @users.add_rmv(User("Mark", "Mark@mail"))
    def test_admins_can_edit_others(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))
        self.assertIn("Select new role for the user", result.data.decode("UTF-8"))
        
    @log_user(1, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_user_listing_allowed_for_admins(self):
        result = self.test_app.get("/view/community")
        self.assertNotIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertNotIn("only admins have access", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_user_listing_raises_403error_if_not_admin(self):
        result = self.test_app.get("/view/community")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("only admins have access", result.data.decode("UTF-8"))

    @log_user(3, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    @users.add_rmv(User("Mark", "Mark@mail"))
    def test_edit_delete_button_allowed_for_admins(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @log_user(1, "Mark", "Mark@mail", "regular")
    @configure(True)
    @users.add_rmv(User("Mark", "Mark@mail"))
    def test_edit_delete_button_allowed_for_owners(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @users.add_rmv(User("Mark", "Mark@mail"))
    def test_edit_delete_button_notallowed_for_others(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertNotIn("Edit info", result.data.decode("UTF-8"))
        self.assertNotIn("Delete account", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @users.add_rmv(User("Mark", "Mark@mail"))
    @configure(True)
    def test_members_cannot_edit_others(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(1, "Mark", "Mark@mail", "regular")
    @users.add_rmv(User("Mark", "Mark@mail"))
    @configure(True)
    def test_members_can_edit_themselves(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))

    @configure(True)
    def test_not_members_cannot_edit_users(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @users.add_rmv(User("Mark", "Mark@mail"))
    @configure(True)
    def test_profile_allowed_for_members(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("John Doe", result.data.decode("UTF-8"))

    @configure(True)
    def test_profile_path_raises_403error_if_not_member(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_users_creation_allowed_for_admins(self):
        result = self.test_app.get("/create")
        self.assertIn("What type of user are you creating", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_users_creation_not_allowed_for_others(self):
        result = self.test_app.get("/create")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("only admins have access", result.data.decode("UTF-8"))

    
        