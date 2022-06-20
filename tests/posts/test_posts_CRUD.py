from urllib.parse import urlparse
from flask import Flask
from pytest import fixture

from services.posts.posts_in_memo import Posts
from tests.helpers import add_disposable_post, configure, get_url_userid, log_user

BASE_POST = "/post/"
CONFIG_PAGE = "/config"
BASE =  "/"

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

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

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_create_redirect(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is a creation test"
    }
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    id = get_url_userid(creation)
    assert creation.status_code == 302
    Posts().remove(id)

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_create_post(client):
    post = {
    "author" : "Mark Doe",
    "title" : "Generic",
    "post" : "This is another creation test"
    }        
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    id = get_url_userid(creation)
    result = client.get(BASE_POST + f"read/{id}/")
    assert post["title"] in result.data.decode("UTF-8")
    assert post["post"] in result.data.decode("UTF-8")
    Posts().remove(id)

@log_user(2, "John Doe", "John@mail", "regular")   
@configure(True)
def test_creation_home_print(client):
    post = {
    "author" : "James Doe",
    "title" : "Generic",
    "post" : "I am printed on home page."
    }
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    id = get_url_userid(creation)
    result = client.get(BASE)
    assert post["post"] in result.data.decode("UTF-8")
    Posts().remove(id)

@configure(True)
def test_read_post(client):
    result = client.get(BASE_POST + "read/1/")
    assert "Written by:Mark Doe" in result.data.decode("UTF-8")
    assert "Generic1" in result.data.decode("UTF-8")
    assert "Test post 1" in result.data.decode("UTF-8")
    
@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_edit_post(client):
    edit = {
    "author" : "John Doe",
    "title" : "Generic",
    "post" : "This is an edit"
    }
    initial = client.get(BASE_POST + "read/4/")
    assert "Test post 1" in initial.data.decode("UTF-8")
    client.post(BASE_POST + "edit/4/", data = edit, follow_redirects=False)
    result = client.get(BASE_POST + "read/4/")
    assert edit["post"] in result.data.decode("UTF-8")

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_delete_post(client):
    id = add_disposable_post()
    read = client.get(BASE_POST + f"read/{id}/")
    assert "John Doe" in read.data.decode("UTF-8")
    assert "Generic" in read.data.decode("UTF-8")
    assert "I will be deleted" in read.data.decode("UTF-8")
    result = client.post(BASE_POST + f"read/{id}", data = {"postID" : id})
    assert "I will be deleted" not in result.data.decode("UTF-8")

@log_user(2, "John Doe", "Generic", "regular")
@configure(True)
def test_redirect_delete(client):
    id = add_disposable_post()
    result = client.post(
        BASE_POST + f"read/{id}/",
        data = {"postID" : id},
        follow_redirects=False)
    assert result.status_code == 302
    assert urlparse(result.location).path == "/"
