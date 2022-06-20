from flask import Flask
from pytest import fixture

from tests.helpers import configure, log_user

BASE_POST = "/post/"

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@log_user(3, "Admin", "admin@admin", "admin")
@configure(True)
def test_admins_can_edit_others(client):
    result = client.get("/edit/1")
    assert "Change profile information" in result.data.decode("UTF-8")
    assert "Select new role for the user" in result.data.decode("UTF-8")
    
@log_user(3, "Admin", "admin@admin", "admin")
@configure(True)
def test_user_listing_allowed_for_admins(client):
    result = client.get("/view/community")
    assert "403 - Forbidden" not in result.data.decode("UTF-8")
    assert "only admins have access" not in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_user_listing_raises_403error_if_not_admin(client):
    result = client.get("/view/community")
    assert "403 - Forbidden" in result.data.decode("UTF-8")
    assert "only admins have access" in result.data.decode("UTF-8")

@log_user(3, "Admin", "admin@admin", "admin")
@configure(True)
def test_edit_delete_button_allowed_for_admins(client):
    result = client.get("/view/1/?pg=1")
    assert "Edit info"in result.data.decode("UTF-8")
    assert "Delete account", result.data.decode("UTF-8")

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_edit_delete_button_allowed_for_owners(client):
    result = client.get("/view/1/?pg=1")
    assert "Edit info" in result.data.decode("UTF-8")
    assert "Delete account" in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
def test_edit_delete_button_notallowed_for_others(client):
    result = client.get("/view/1/?pg=1")
    assert "Edit info" not in result.data.decode("UTF-8")
    assert "Delete account" not in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_members_cannot_edit_others(client):
    result = client.get("/edit/1")
    assert "405 - Method Not Allowed" in result.data.decode("UTF-8")
    assert "You do not have necessary authorization for editting" in result.data.decode("UTF-8")

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_members_can_edit_themselves(client):
    result = client.get("/edit/1")
    assert "Change profile information" in result.data.decode("UTF-8")

@configure(True)
def test_not_members_cannot_edit_users(client):
    result = client.get("/edit/1")
    assert "405 - Method Not Allowed" in result.data.decode("UTF-8")
    assert "You do not have necessary authorization for editting" in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_profile_allowed_for_members(client):
    result = client.get("/view/1/?pg=1")
    assert result.status_code == 200
    assert "John Doe" in result.data.decode("UTF-8")

@configure(True)
def test_profile_path_raises_403error_if_not_logged(client):
    result = client.get("/view/1/?pg=1")
    assert "403 - Forbidden" in result.data.decode("UTF-8")

@log_user(3, "Admin", "admin@admin", "admin")
@configure(True)
def test_users_creation_allowed_for_admins(client):
    result = client.get("/create")
    assert "What type of user are you creating" in result.data.decode("UTF-8")

@log_user(1, "John Doe", "John@mail", "regular")
@configure(True)
def test_users_creation_not_allowed_for_others(client):
    result = client.get("/create")
    assert "403 - Forbidden" in result.data.decode("UTF-8")
    assert "only admins have access" in result.data.decode("UTF-8")