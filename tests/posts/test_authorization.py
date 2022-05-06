import unittest
from flask import current_app, url_for
from __initblog__ import create_blog
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo
from tests.test_helpers import configure, delete_post, log_user, create_user, create_posts, logout_login

class AuthorizationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()
            
    @Services.get
    def get_posts(self, posts : IPostRepo):
        return posts

    @log_user(1, "John Doe", "JDoe@gmail", "regular")
    @configure(True)
    def test_admins_can_edit_others_posts(self):
        create_posts(self, "John Doe", 1)
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
                session["id"] = "3"
                session["username"] = "admin"
                session["email"] = "admin@admin"
                session["role"] = "admin"
        result = self.test_app.get("/post/edit/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertIn("Edit Post", result.data.decode("UTF-8"))
        self.assertIn("Current Title", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@gmail", "regular")
    @configure(True)
    def test_edit_delete_button_allowed_for_admins(self):
        create_posts(self, "John Doe", 1)
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
                session["id"] = "3"
                session["username"] = "admin"
                session["email"] = "admin@admin"
                session["role"] = "admin"
        result = self.test_app.get("/post/read/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertIn("Edit", result.data.decode("UTF-8"))
        self.assertIn("Delete", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_edit_delete_button_allowed_for_owners(self):
        create_posts(self, "John Doe", 1)
        result = self.test_app.get("post/read/2")
        self.assertIn("Edit", result.data.decode("UTF-8"))
        self.assertIn("Delete", result.data.decode("UTF-8"))
    
    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_edit_delete_button_notallowed_for_notmembers(self):
        create_posts(self, "John Doe", 1)
        self.test_app.get(url_for("authentication.log_out"))
        result = self.test_app.get("post/read/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertNotIn("Edit", result.data.decode("UTF-8"))
        self.assertNotIn("Delete", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_edit_delete_button_notallowed_for_notowners(self):
        create_posts(self, "John Doe", 1)
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
            session["id"] = "3"
            session["username"] = "James"
            session["email"] = "James@mail"
            session["role"] = "regular"
        result = self.test_app.get("post/read/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertNotIn("Edit", result.data.decode("UTF-8"))
        self.assertNotIn("Delete", result.data.decode("UTF-8"))

    @configure(True)
    def test_not_members_cannot_create_new_posts(self):
        result = self.test_app.get("/post/create")
        self.assertIn("403 - Forbidden", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_can_create_new_posts(self):
        result = self.test_app.get("/post/create")
        self.assertNotIn("403 - Forbidden", result.data.decode("UTF-8"))
        self.assertIn("Add a title", result.data.decode("UTF-8"))
        
    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others_post(self):
        create_posts(self, "John Doe", 1)
        logout_login(self, "Mark@mail")
        result = self.test_app.get("/post/edit/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_members_can_edit_owned_post(self):
        create_posts(self, "John Doe", 1)
        result = self.test_app.get("/post/edit/2")
        delete_post(self.get_posts(IPostRepo), 2)
        self.assertIn("Edit Post", result.data.decode("UTF-8"))
        self.assertIn("Current Title", result.data.decode("UTF-8"))
        