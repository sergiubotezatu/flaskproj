from urllib.parse import urlparse
from flask import Flask
from pytest import fixture
import __init__
from services.interfaces.ipost_repo import IPostRepo
from tests.helpers import configure, log_user, RepoMngr

BASE_POST = "/post/"
CONFIG_PAGE = "/config"
BASE =  "/"

@fixture()
def app() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    posts = RepoMngr(IPostRepo)
    posts.create_posts_db(3)
    yield app

@fixture()
def client(app):
    return app.test_client()

@configure(True)
def test_setuppage_redirects_if_configured(client):
    result = client.get(CONFIG_PAGE, follow_redirects = False)
    assert result.status_code == 302

@configure(False)
def test_setuppage_doesnt_redirect_if_notconfig(client):
    result = client.get(CONFIG_PAGE, follow_redirects = False)
    assert result.status_code == 200

@configure(False)
def test_home_redirects_tosetup_if_notConfig(client):
    result = client.get(BASE, follow_redirects = True)
    assert "host" in result.data.decode("UTF-8")

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
def test_create_post(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is a test"
    }        
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=True)
    assert post["title"] in creation.data.decode("UTF-8")
    assert post["post"] in creation.data.decode("UTF-8")

@log_user(3, "James Doe", "Mark@email.com", "regular")   
@configure(True)
def test_creation_home_print(client):
    post = {
    "author" : "James Doe",
    "title" : "Generic",
    "post" : "I am printed on home page."
    }
    client.post(BASE_POST + "create", data = post)
    result = client.get(BASE)
    assert post["post"] in result.data.decode("UTF-8")


@log_user(2, "John Doe", "Mark@email.com", "regular")
@configure(True)
def test_edit_post(client):
    edit = {
    "author" : "John Doe",
    "title" : "Generic",
    "post" : "This is an edit"
    }
    initial = client.get(BASE_POST + "read/3/")
    assert "Test post 3" in initial.data.decode("UTF-8")
    client.post(BASE_POST + "edit/3", data = edit, follow_redirects=True)
    result = client.get(BASE_POST + "read/3/")
    assert edit["post"] in result.data.decode("UTF-8")


@log_user(2, "John Doe", "JDoe@email.com", "regular")
@configure(True)
def test_delete_post(client):
    post = {
    "author" : "John Doe",
    "title" : "Generic",
    "post" : "Test post 1"
    }
    read = client.get(BASE_POST + "read/1/")
    assert post["author"] in  read.data.decode("UTF-8")
    assert post["title"] in  read.data.decode("UTF-8")
    assert post["post"] in read.data.decode("UTF-8")
    result = client.post(BASE_POST + "read/1", data = {"postID" : "1"})
    assert post["author"] not in result.data.decode("UTF-8")


@log_user(2, "John Doe", "Generic", "regular")
@configure(True)
def test_redirect_delete(client):
    result = client.post(
        BASE_POST + "read/2/",
        data = {"postID" : "2"},
        follow_redirects=False)
    assert result.status_code == 302
    assert urlparse(result.location).path == "/"
