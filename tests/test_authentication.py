from flask import Flask
from pytest import fixture
import __init__
from services.interfaces.ipost_repo import IPostRepo
from tests.helpers import configure, log_user, RepoMngr

auth_info = {
        "mail" : "JDoe@mail",
        "pwd" : "password1@",
        }

USER = {
    "username" : "John Doe",
    "email" : "JDoe@mail",
    "pwd" : "password1@"
    }

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3)
    yield app
    posts.clear()

@fixture()
def client(app):
    return app.test_client()

@configure(False)
def test_redirects_tosetup_if_notConfig(client):
    result = client.get("/login", follow_redirects = True)
    assert "host" in result.data.decode("UTF-8")

@configure(True)
def test_login_request(client):
    result = client.get("/login")
    assert result.status_code == 200

@configure(True)
def test_login_redirect_if_already_logged(client):
    client.post("/signup", data = USER, follow_redirects=True)
    login = client.post("/login", data = auth_info, follow_redirects=False)
    result = client.get(login.location)
    assert "You are already logged" in result.data.decode("UTF-8")

@log_user(1, "John Doe", "JDoe@mail", "regular")
@configure(True)
def test_logout_pops_user_from_session(client):
    with client.session_transaction() as session:
        assert 1 == session["id"]
    client.get("/logout")
    with client.session_transaction() as session:
        assert "id" not in session

@configure(True)
def test_login_adds_user_into_session(client):
    client.post("/signup", data = USER, follow_redirects=True)
    client.get("/logout")
    client.post("/login", data = auth_info, follow_redirects=False)
    with client.session_transaction() as session:
        assert session["id"] == 1
        assert session["username"] == "John Doe"
        assert session["email"] == "JDoe@mail"
        assert session["role"] == "regular"

@configure(True)
def test_login_fails_wrong_email(client):
    client.post("/signup", data = USER, follow_redirects=True)
    wrong_mail = {
    "mail" : "JDoe@gmail",
    "pwd" : "password1@",
    }
    client.get("/logout")
    login = client.post("/login", data = wrong_mail, follow_redirects=True)
    assert "Incorrect Password or Email. Please try again" in login.data.decode("UTF-8")

@configure(True)
def test_login_fails_wrong_password(client):
    client.post("/signup", data = USER, follow_redirects=True)
    wrong_pass = {
    "mail" : "John@mail",
    "pwd" : "pass1@",
    }
    client.get("/logout")
    login = client.post("/login", data = wrong_pass, follow_redirects=False)
    assert "Incorrect Password or Email. Please try again" in login.data.decode("UTF-8")
    
@configure(True)
def test_user_displayed_on_navbar(client):
    client.post("/signup", data = USER, follow_redirects=True)
    client.post("/login", data = auth_info, follow_redirects=False)
    home = client.get("/")
    assert "John Doe" in home.data.decode("UTF-8")