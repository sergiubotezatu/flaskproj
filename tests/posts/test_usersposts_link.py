import unittest
from flask import current_app
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, log_user, create_posts, create_user

class PostsUsersLinkTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    posts = RepoMngr(IPostRepo)
    users = RepoMngr(IUsersRepo)
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_ownerId_from_logged_user(self):
        create_posts(self, "John", 3)
        posts = self.posts.repo.get_all()
        self.assertEqual(posts[0][1].owner_id, 2)
        self.posts.delete(1)
    
    @log_user(2, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_name_from_logged_user(self):
        result = self.test_app.get("/post/create")
        self.assertIn("John Doe", result.data.decode("UTF-8"))
        
    @configure(True)
    def test_editting_user_reflects_in_posts(self):
        create_user(self, "Mark Doe", "Mdoe@email")
        create_posts(self, "Mark Doe", 1)
        edit = {
        "username" : "James Doe",
        "email" : "Mdoe@email",
        "pwd" : "password1@",
        "oldpass" : "password1@"
        }
        self.test_app.post("/edit/1", data = edit, follow_redirects=True)
        posts = self.posts.repo.get_all()
        self.posts.delete(1)
        self.users.delete(id = 1)
        self.assertEqual("James Doe", posts[0][1].auth)
    
    @configure(True)
    def test_deleting_user_deletes_owned_posts(self):
        create_user(self, "Mark Doe", "Mdoe@email")
        create_posts(self, "Mark Doe", 1)
        self.test_app.post("view/1/?pg=1", data = {"userID" : "1"}, follow_redirects = False)
        posts = self.posts.repo.get_all()
        self.assertEqual(len(posts), 0)
        