from urllib.parse import urlparse
from flask import Flask
from pytest import fixture
import __init__
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from services.users.users_in_memo import Users
from tests.helpers import configure, log_user, RepoMngr

BASE_POST = "/post/"

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    users = RepoMngr(IUsersRepo)
    users.add(User("Mark Doe", "Mark@mail"))
    users.add(User("James Doe", "James@mail"))
    users.add(User("Joey Doe", "Joseph@mail"))
    users.add(User("Ross Geller", "Ross@museum"))
    yield app
        
def fun (x = 5):
    return x

@fixture()
def client(app):
    return app.test_client()

@configure(True)
def test_create_user(client):
    user = {
    "username" : "John Doe",
    "email" : "JDoe@John",
    "pwd" : "password1@"
    }        
    
    creation = client.post("/signup", data = user, follow_redirects=True)
    page = creation.data.decode("UTF-8")
    assert user["username"] in page
    assert user["email"] in page
    
@log_user(2, "James Doe", "James@mail", "regular")
@configure(True)
def test_delete_user(client):
    profile_pg = client.get("view/2/?pg=1")
    result = client.post("view/2/?pg=1", data = {"userID" : "2"}, follow_redirects = False)
    empty_pg = client.get("view/2/?pg=1")
    assert "/" == urlparse(result.location).path
    assert "James Doe" in profile_pg.data.decode("UTF-8")
    assert "James Doe" not in empty_pg.data.decode("UTF-8")
        
@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_edit_user(client):
    edit = {
    "username" : "Markus",
    "email" : "MDoe@John",
    "pwd" : "password1@",
    "oldpass" : ""
    }
    client.post("/edit/1", data = edit, follow_redirects=True)
    result = client.get("/view/1/?pg=1")
    assert edit["username"] in result.data.decode("UTF-8")
    
@configure(True)
@log_user(1, "Mark Doe", "Mark@mail", "regular")
def test_profile_request(client):
    result = client.get("/view/1/?pg=1")
    assert result.status_code == 200

@configure(True)
@log_user(1, "Mark Doe", "Mark@mail", "regular")
def test_read_user(client):
    read_user = client.get("/view/1/?pg=1")
    assert "Mark Doe" in read_user.data.decode("UTF-8")

@configure(True)
@log_user(1, "Mark Doe", "MDoe@John", "admin")
def test_users_show_in_user_listing(client):
    read_users = client.get("/view/community")
    assert "Joey Doe" in read_users.data.decode("UTF-8")

@configure(True)
@log_user(1, "Mark Doe", "MDoe@John", "admin")
def test_deleted_show_in_user_listing(client):
    client.post("/view/4/?pg=1", data = {"userID" : "4"})
    read_users = client.get("/view/community")
    assert "Ross@museum" in read_users.data.decode("UTF-8")
    
@configure(False)
@log_user(1, "Mark Doe", "MDoe@John", "admin")
def test_redirects_tosetup_if_notConfig(client):
    result = client.get("/view/1/?pg=1", follow_redirects = True)
    assert "host" in result.data.decode("UTF-8")