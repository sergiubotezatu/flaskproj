import unittest
from flask import current_app
from __initblog__ import create_blog
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo
from tests.test_tools import configure, log_user, create_posts, create_user

class PostsUsersLinkTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    @Services.get
    def get_posts(self, posts : IPostRepo):
        return posts
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_ownerId_from_logged_user(self):
        create_posts(self, "John", 3)
        posts = self.get_posts(IPostRepo).get_all()
        for post in posts:
            if post[1].auth == "John":
                self.assertEqual("2", post[1].owner_id)
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_name_from_logged_user(self):
        result = self.test_app.get("/post/create")
        self.assertIn("John Doe", result.data.decode("UTF-8"))

    @configure(True)
    def test_editting_ownerId_reflects_in_posts(self):
        create_user(self, "Mark Doe", "JDoe@John")
        create_posts(self, "Mark Doe", 1)
        edit = {
        "username" : "James Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@",
        "oldpass" : "password1@"
        }
        self.test_app.post("/edit/1", data = edit, follow_redirects=True)
        posts = self.get_posts(IPostRepo).get_all()
        for post in posts:
            if post[1].owner_id == "2":
                self.assertEqual("James Doe", posts[1].auth)

    @configure(True)
    def test_deleting_user_deletes_owned_posts(self):
        self.test_app.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
        posts = self.get_posts(IPostRepo)
        for post in posts:
            self.assertNotEqual("James", post.auth)
