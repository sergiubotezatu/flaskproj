from urllib.parse import urlparse
from flask import Flask
from pytest import fixture

from models.user import User
from services.users.users_in_memo import Users
from tests.helpers import add_disposable_user, configure, get_url_userid, log_user

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@configure(True)
def test_create_user(client):
    user = {
    "username" : "John Doe",
    "email" : "JDoe@John",
    "pwd" : "password1@"
    }
    creation = client.post("/signup", data = user, follow_redirects=False)
    id = get_url_userid(creation)
    result = client.get(creation.location)
    page = result.data.decode("UTF-8")
    assert user["username"] in page
    assert user["email"] in page
    Users().remove(id)
    
@log_user(3, "James Doe", "James@mail", "regular")
@configure(True)
def test_delete_user(client):
    new_id = add_disposable_user()
    profile_pg = client.get(f"view/{new_id}/?pg=1")
    result = client.post(f"view/{new_id}/?pg=1", data = {"userID" : new_id}, follow_redirects = False)
    empty_pg = client.get(f"view/{new_id}/?pg=1")
    assert "/" == urlparse(result.location).path
    assert "James Doe" in profile_pg.data.decode("UTF-8")
    assert "James Doe" not in empty_pg.data.decode("UTF-8")
    
@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_edit_user(client):
    edit = {
    "username" : "Markus",
    "email" : "Mark@mail",
    "pwd" : "password1@",
    "oldpass" : ""
    }
    client.post("/edit/1", data = edit, follow_redirects=True)
    result = client.get("/view/1/?pg=1")
    assert edit["username"] in result.data.decode("UTF-8")
    Users().update(1, User("Mark Doe", "Mark@mail"))
    
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
@log_user(3, "Admin", "admin@mail", "admin")
def test_users_show_in_user_listing(client):
    read_users = client.get("/view/community")
    assert "John Doe" in read_users.data.decode("UTF-8")
    assert "Mark Doe" in read_users.data.decode("UTF-8")

@configure(True)
@log_user(3, "Admin", "admin@mail", "admin")
def test_deleted_show_in_user_listing(client):
    new_id = add_disposable_user()
    client.post(f"/view/{new_id}/?pg=1", data = {"userID" : new_id})
    read_users = client.get("/view/community")
    assert "James@mail" in read_users.data.decode("UTF-8")
    
@configure(False)
@log_user(1, "Mark Doe", "Mark@mail", "regular")
def test_redirects_tosetup_if_notConfig(client):
    result = client.get("/view/1/?pg=1", follow_redirects = True)
    assert "host" in result.data.decode("UTF-8")