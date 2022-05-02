import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.database.database import DataBase

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self):
            with self.test_app.session_transaction() as session:
                session["id"] = str(id)
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(self)
        return wrapper
    return decorator

def configure(is_config : bool):
    def decorator(test_func):
        def wrapper(self):
            DataBase.config.is_configured = is_config
            return test_func(self)
        return wrapper
    return decorator

class AuthorizationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def create_user(self, name, mail):
        user = {
                "username" : name,
                "email" : mail,
                "pwd" : "password1@"
                }
        self.test_app.post("/signup", data = user, follow_redirects=False)

    def create_post(self, name):
        post = {
        "author" : name,
        "title" : "Generic",
        "post" : "This is a test"
        }
        self.test_app.post("/post/create", data = post, follow_redirects=False)

    def logout_login(self, mail):
        user = {
            "email" : mail,
            "pwd" : "password1@"
        }
        self.test_app.get(url_for("authentication.log_out"))
        self.test_app.post("/login", data = user, follow_redirects=False)

    @configure(True)
    def test_admins_can_edit_others(self):
        self.create_user("Mark", "Mark@mail")
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
                session["id"] = "3"
                session["username"] = "admin"
                session["email"] = "admin@admin"
                session["role"] = "admin" 
        result = self.test_app.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))
        self.assertIn("Select new role for the user", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@gmail", "regular")
    @configure(True)
    def test_admins_can_edit_others_posts(self):
        self.create_post("John Doe")
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
                session["id"] = "3"
                session["username"] = "admin"
                session["email"] = "admin@admin"
                session["role"] = "admin"
        result = self.test_app.get("/post/edit/2")
        self.assertIn("Edit Post", result.data.decode("UTF-8"))
        self.assertIn("Current Title", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "admin")
    @configure(True)
    def test_community_allowed_for_admins(self):
        result = self.test_app.get("/view/community")
        self.assertNotIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertNotIn("only admins have access", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_community_raises_403error_if_not_admin(self):
        result = self.test_app.get("/view/community")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("only admins have access", result.data.decode("UTF-8"))

    @log_user(3, "John Doe", "JDoe@mail", "admin")
    def test_edit_delete_button_allowed_for_admins(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @log_user(1, "Mark", "Mark@mail", "regular")
    def test_edit_delete_button_allowed_for_owners(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertIn("Edit info", result.data.decode("UTF-8"))
        self.assertIn("Delete account", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    def test_edit_delete_button_notallowed_for_others(self):
        result = self.test_app.get("/view/1/?pg=1")
        self.assertNotIn("Edit info", result.data.decode("UTF-8"))
        self.assertNotIn("Delete account", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others_post(self):
        self.create_post("John Doe")
        self.logout_login("Mark@mail")
        result = self.test_app.get("/post/edit/Jo1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_can_edit_owned_post(self):
        self.create_post("John Doe")
        result = self.test_app.get("/post/edit/3")
        self.assertIn("Edit Post", result.data.decode("UTF-8"))
        self.assertIn("Current Title", result.data.decode("UTF-8"))
    
    @log_user(1, "Mark", "Mark@mail", "regular")
    @configure(True)
    def test_members_can_edit_themselves(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("Change profile information", result.data.decode("UTF-8"))

    @configure(True)
    def test_not_members_cannot_edit_users(self):
        result = self.test_app.get("/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
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

    
        