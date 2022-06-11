from flask import Flask
from pytest import fixture
import __init__
from models.post import Post
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from services.posts.posts_in_memo import Posts
from tests.helpers import configure, create_posts, log_user, RepoMngr

BASE_POST = "/post/"

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    posts = RepoMngr(IPostRepo)
    users = RepoMngr(IUsersRepo)
    users.add(User("Mark Doe", "Mdoe@email"))
    users.add(User("James Doe", "James@mail"))
    posts.add(Post("Mark Doe", "Generic", "Test post", owner_id = 1))
    posts.create_posts_db(2, "James Doe", owner_id= 2)
    yield app

@fixture()
def client(app):
    return app.test_client()

@log_user(3, "John Doe", "John@mail", "regular")
@configure(True)
def test_posts_get_ownerId_from_logged_user(client):
    create_posts(client, "John", 1)
    posts = Posts().get_all()
    assert posts[0][1].owner_id == 3

@log_user(3, "John Doe", "John@mail", "regular")
@configure(True)
def test_posts_get_name_from_logged_user(client):
    result = client.get("/post/create")
    assert "John Doe" in result.data.decode("UTF-8")

@log_user(1, "Mark Doe", "Mdoe@email", "regular")
@configure(True)
def test_editting_user_reflects_in_posts(client):
    edit = {
    "username" : "Jimmy Doe",
    "email" : "Mdoe@email",
    "pwd" : "password1@",
    "oldpass" : ""
    }
    client.post("/edit/1", data = edit, follow_redirects=True)
    posts = Posts().get_all()
    for post in posts:
        if post[0] == 1:
            assert "Jimmy Doe", post[1].auth

@log_user(2, "James Doe", "James@mail", "regular")
@configure(True)
def test_deleting_user_deletes_owned_posts(client):
    client.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
    posts = Posts().get_all()
    for post in posts:
        assert "James Doe" != post[1].auth
