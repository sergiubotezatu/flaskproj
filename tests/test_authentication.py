from flask import Flask
from pytest import fixture
import __init__
from tests.helpers import configure, log_user

auth_info = {
        "mail" : "John@mail",
        "pwd" : "password1@",
        }

USER = {
    "username" : "John Doe",
    "email" : "John@mail",
    "pwd" : "password1@"
    }

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@configure(False)
def test_redirects_tosetup_if_notConfig(client):
    result = client.get("/login", follow_redirects = True)
    assert "host" in result.data.decode("UTF-8")

@configure(True)
def test_login_request(client):
    result = client.get("/login")
    assert result.status_code == 200

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_login_redirect_if_already_logged(client):
    login = client.post("/login", data = auth_info, follow_redirects=False)
    result = client.get(login.location)
    assert "You are already logged" in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_logout_pops_user_from_session(client):
    with client.session_transaction() as session:
        assert 2 == session["id"]
    client.get("/logout")
    with client.session_transaction() as session:
        assert "id" not in session

@configure(True)
def test_login_adds_user_into_session(client):
    client.post("/login", data = auth_info, follow_redirects=False)
    with client.session_transaction() as session:
        assert session["id"] == 2
        assert session["username"] == "John Doe"
        assert session["email"] == "John@mail"
        assert session["role"] == "regular"

@configure(True)
def test_login_fails_wrong_email(client):
    wrong_mail = {
    "mail" : "JDoe@gmail",
    "pwd" : "password1@",
    }
    login = client.post("/login", data = wrong_mail, follow_redirects=True)
    assert "Incorrect Password or Email. Please try again" in login.data.decode("UTF-8")

@configure(True)
def test_login_fails_wrong_password(client):
    wrong_pass = {
    "mail" : "John@mail",
    "pwd" : "pass1@",
    }
    login = client.post("/login", data = wrong_pass, follow_redirects=False)
    assert "Incorrect Password or Email. Please try again" in login.data.decode("UTF-8")
    
@configure(True)
def test_user_displayed_on_navbar(client):
    client.post("/login", data = auth_info, follow_redirects=False)
    home = client.get("/")
    assert "John Doe" in home.data.decode("UTF-8")