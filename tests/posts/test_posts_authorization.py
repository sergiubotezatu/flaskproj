from flask import Flask
from pytest import fixture

from tests.helpers import configure, log_user

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@log_user(1, "Mark Doe", "Mark@gmail", "admin")
@configure(True)
def test_admins_can_edit_others_posts(client):
    result = client.get("/post/edit/1/")
    assert "Edit Post" in result.data.decode("UTF-8")
    assert "Current Title" in result.data.decode("UTF-8")

@log_user(1, "Mark Doe", "Mark@gmail", "admin")
@configure(True)
def test_edit_delete_button_allowed_for_admins(client):
    result = client.get("/post/read/1/")
    assert "Edit" in result.data.decode("UTF-8")
    assert "Delete" in result.data.decode("UTF-8")

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_edit_delete_button_allowed_for_owners(client):
    result = client.get("post/read/1/")
    assert "Edit" in result.data.decode("UTF-8")
    assert "Delete" in result.data.decode("UTF-8")

@configure(True)
def test_edit_delete_button_notallowed_for_notmembers(client):
    result = client.get("post/read/1/")
    assert "Edit" not in result.data.decode("UTF-8")
    assert "Delete" not in result.data.decode("UTF-8")

@configure(True)
def test_not_members_cannot_create_new_posts(client):
    result = client.get("/post/create")
    assert "403 - Forbidden" in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_members_can_create_new_posts(client):
    result = client.get("/post/create")
    assert "403 - Forbidden" not in result.data.decode("UTF-8")
    assert "Add a title" in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_members_cannot_edit_others_post(client):
    result = client.get("/post/edit/1/")
    assert "405 - Method Not Allowed" in result.data.decode("UTF-8")
    assert "You do not have necessary authorization for editting" in result.data.decode("UTF-8")

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_members_can_edit_owned_post(client):
    result = client.get("/post/edit/1/")
    assert "Current Title" in result.data.decode("UTF-8")