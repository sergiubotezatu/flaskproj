from flask import Flask
from pytest import fixture
import __init__
from services.interfaces.ipost_repo import IPostRepo
from tests.helpers import configure, log_user, RepoMngr

BASE_POST = "/post/"

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3)
    yield app

@fixture()
def client(app):
    return app.test_client()


@log_user(3, "Mark Doe", "Mark@email.com", "regular")
@configure(True)
def test_create_redirect(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is a test"
    }
    result = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    assert result.status_code == 302

@log_user(3, "Mark Doe", "Mark@email.com", "regular")
@configure(True)
def test_create(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is a test"
    }
    result = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    assert 2 == 302