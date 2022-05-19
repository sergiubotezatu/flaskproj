import unittest
from flask.testing import FlaskClient
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, configure, getClient, log_user, create_posts

class PostsUsersLinkTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)


    posts = RepoMngr(IPostRepo)
    users = RepoMngr(IUsersRepo)
    users.add(User("Mark Doe", "Mdoe@email"))
    users.add(User("James Doe", "James@mail"))
    posts.add(Post("Mark Doe", "Generic", "Test post", owner_id = 1))
    posts.create_posts_db(2, "James Doe", owner_id= 2)
    
    @getClient
    @log_user(3, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_ownerId_from_logged_user(self, client : FlaskClient = None):
        create_posts(client, "John", 1)
        posts = self.posts.repo.get_all()
        self.assertEqual(posts[0][1].owner_id, 3)
    
    @getClient
    @log_user(3, "John Doe", "John@mail", "regular")
    @configure(True)
    def test_posts_get_name_from_logged_user(self, client : FlaskClient = None):
        result = client.get("/post/create")
        self.assertIn("John Doe", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "Mark Doe", "Mdoe@email", "regular")
    @configure(True)
    def test_editting_user_reflects_in_posts(self, client : FlaskClient = None):
        edit = {
        "username" : "Jimmy Doe",
        "email" : "Mdoe@email",
        "pwd" : "password1@",
        "oldpass" : ""
        }
        client.post("/edit/1", data = edit, follow_redirects=True)
        posts = self.posts.repo.get_all()
        for post in posts:
            if post[0] == 1:
                self.assertEqual("Jimmy Doe", post[1].auth)

    @getClient
    @log_user(2, "James Doe", "James@mail", "regular")
    @configure(True)
    def test_deleting_user_deletes_owned_posts(self, client : FlaskClient = None):
        client.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
        posts = self.posts.repo.get_all()
        for post in posts:
            self.assertNotEqual("James Doe", post[1].auth)
        