from flask import Flask
from pytest import fixture
import __init__
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.helpers import RepoMngr, configure, create_posts, log_user

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    yield app

@fixture()
def client(app):
    return app.test_client()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_next_button_available_if_more_posts(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 6)
    home_pg = client.get("/")
    assert "Next" in home_pg.data.decode("UTF-8")
    assert "&raquo;" in home_pg.data.decode("UTF-8")
    posts.clear()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_next_button_notavailable_if_less_than_6posts(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 5)
    home_pg = client.get("/")
    assert "Next &raquo;" not in home_pg.data.decode("UTF-8")
    posts.clear()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_only_5posts_displayed_on_pg(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 6)
    home_pg = client.get("/")
    assert "Generic5" in home_pg.data.decode("UTF-8")
    assert "Generic4" in home_pg.data.decode("UTF-8")
    assert "Generic3" in home_pg.data.decode("UTF-8")
    assert "Generic2" in home_pg.data.decode("UTF-8")
    assert "Generic1" in home_pg.data.decode("UTF-8")
    assert "Generic0" not in home_pg.data.decode("UTF-8")
    posts.clear()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_previous_button_available_on_second_pg(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 6)
    home_pg = client.get("/?pg=2")
    assert("&laquo; Previous", home_pg.data.decode("UTF-8"))
    posts.clear()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_previous_button_notavailable_on_first_pg(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 2)
    home_pg = client.get("/")
    assert "&laquo; Previous" not in home_pg.data.decode("UTF-8")
    posts.clear()

@log_user(2, "John", "John@mail", "regular")
@configure(True)
def test_previous_and_next_available_middle_pg(client):
    posts = RepoMngr(IPostRepo)
    create_posts(client, "John", 11)
    home_pg = client.get("/?pg=2")
    assert("&laquo; Previous", home_pg.data.decode("UTF-8"))
    assert("Next", home_pg.data.decode("UTF-8"))
    posts.clear()