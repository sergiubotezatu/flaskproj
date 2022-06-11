from flask import Flask
from pytest import fixture
import __init__
from models.user import User
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo
from tests.helpers import configure, RepoMngr

BASE_POST = "/post/"

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    users = RepoMngr(IUsersRepo)
    posts = RepoMngr(IPostRepo)
    users.add(User("John", "jodhn@mail"))
    users.add(User("Markus", "markus@mail"))
    users.add(User("James", "james@mail"))
    posts.create_posts_db(3, "John", 1)
    posts.create_posts_db(3, "Markus", 2)
    posts.create_posts_db(3, "James", 3)
    yield app
    users.clear()
    posts.clear()

@fixture()
def client(app):
    return app.test_client()

@configure(True)
def test_front_pg_displays_all_filterable_users(client):
    result = client.get("/")
    assert '<a href="/?user_id=1&amp;name=John&amp;">John</a>' in result.data.decode("UTF-8")
    assert '<a href="/?user_id=2&amp;name=Markus&amp;">Markus</a>' in result.data.decode("UTF-8")
    assert '<a href="/?user_id=3&amp;name=James&amp;">James</a>'in result.data.decode("UTF-8")        

@configure(True)
def test_front_pg_displays_only_filtered_users_post(client):
    unfiltered_home = client.get("/")
    assert 2 ==  unfiltered_home.data.decode("UTF-8").count("by Markus")
    filtered = client.get("/?user_id=1&name=John&")
    assert 0 == filtered.data.decode("UTF-8").count("by Markus")
    assert 3 == filtered.data.decode("UTF-8").count("by John")

@configure(True)
def test_front_pg_displays_multiple_filtered_users(client):
    filtered = client.get("/?user_id=1&name=John&user_id=3&name=James")
    assert 2 == filtered.data.decode("UTF-8").count("by John")
    assert 3 == filtered.data.decode("UTF-8").count("by James")

@configure(True)
def test_page_change_doesnot_affect_filters(client):
    filtered = client.get("/?user_id=1&name=John&user_id=3&name=James&pg=2")
    assert 1 == filtered.data.decode("UTF-8").count("by John")
    assert 0 == filtered.data.decode("UTF-8").count("by James")