import unittest
from flask import current_app
from __initblog__ import create_blog
from services.interfaces.ipost_repo import IPostRepo
from tests.test_helpers import configure, log_user, RepoMngr

class AuthorizationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()
            
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3)

    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_admins_can_edit_others_posts(self):
        result = self.test_app.get("/post/edit/1")
        self.assertIn("Edit Post", result.data.decode("UTF-8"))
        self.assertIn("Current Title", result.data.decode("UTF-8"))

    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_edit_delete_button_allowed_for_admins(self):
        result = self.test_app.get("/post/read/1/")
        self.assertIn("Edit", result.data.decode("UTF-8"))
        self.assertIn("Delete", result.data.decode("UTF-8"))

    @log_user(2, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_edit_delete_button_allowed_for_owners(self):
        result = self.test_app.get("post/read/1/")
        self.assertIn("Edit", result.data.decode("UTF-8"))
        self.assertIn("Delete", result.data.decode("UTF-8"))
    
    @configure(True)
    def test_edit_delete_button_notallowed_for_notmembers(self):
        result = self.test_app.get("post/read/1/")
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
        
    @log_user(1, "Greg Doe", "GDoe@mail", "regular")
    @configure(True)
    def test_members_cannot_edit_others_post(self):
        result = self.test_app.get("/post/edit/1")
        self.assertIn("405 - Method Not Allowed", result.data.decode("UTF-8"))
        self.assertIn("You do not have necessary authorization for editting", result.data.decode("UTF-8"))

    @log_user(2, "Mark Doe", "MDoe@mail", "regular")
    @configure(True)
    def test_members_can_edit_owned_post(self):
        result = self.test_app.get("/post/edit/1")
        self.assertIn("Current Title", result.data.decode("UTF-8"))
        