from flask import Flask
from pytest import fixture

from models.user import User
from services.posts.posts_in_memo import Posts
from services.users.users_in_memo import Users
from tests.helpers import add_disposable_user, configure, get_url_userid, log_user

BASE_POST = "/post/"

@fixture()
def client(data_base) -> Flask:
    return data_base.test_client()

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_posts_get_ownerId_from_logged_user(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is a creation test"
    }
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    id = get_url_userid(creation)
    assert Posts().get(id).owner_id == 2
    Posts().remove(id)

@log_user(3, "John Doe", "John@mail", "regular")
@configure(True)
def test_posts_get_name_from_logged_user(client):
    result = client.get("/post/create")
    assert "John Doe" in result.data.decode("UTF-8")

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_editting_user_reflects_in_post(client):
    edit = {
    "username" : "Jimmy Doe",
    "mail" : "Mark@mail",
    "pwd" : "password1@",
    "oldpass" : ""
    }
    client.post("/edit/1", data = edit, follow_redirects=False)
    assert "Jimmy Doe" in client.get(BASE_POST + "read/1/").data.decode("UTF-8")
    Users().update(1, User("Mark Doe", "Mark@mail"))
    
@log_user(2, "James Doe", "James@mail", "regular")
@configure(True)
def test_deleting_user_deletes_owned_posts(client):
    id = str(add_disposable_user())
    client.post(f"view/{id}/?pg=1", data = {"userID" : id}, follow_redirects = False)
    posts = Posts().get_all()
    for post in posts:
        assert "James Doe" != post[1].auth
