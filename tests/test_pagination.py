from flask import Flask
from pytest import fixture
import __init__
from services.interfaces.ipost_repo import IPostRepo
from services.posts.posts_in_memo import Posts
from services.users.users_in_memo import Users
from tests.helpers import add_disposable_post, configure, log_user

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_next_button_available_if_more_posts(client):
    home_pg = client.get("/")
    assert "Next" in home_pg.data.decode("UTF-8")
    assert "&raquo;" in home_pg.data.decode("UTF-8")
    
@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_next_button_notavailable_if_less_than_6posts(client):
    client.post("/post/read/6/", data = {"postID" : 6})
    home_pg = client.get("/")
    assert "Next &raquo;" not in home_pg.data.decode("UTF-8")
    post = {
    "author" : "John Doe",
    "title" : "Generic6",
    "post" : "Test post 3"
    }
    client.post("/post/create", data=post)

@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_only_5posts_displayed_on_pg(client):
    home_pg = client.get("/")
    assert "Generic6" in home_pg.data.decode("UTF-8")
    assert "Generic5" in home_pg.data.decode("UTF-8")
    assert "Generic4" in home_pg.data.decode("UTF-8")
    assert "Generic3" in home_pg.data.decode("UTF-8")
    assert "Generic2" in home_pg.data.decode("UTF-8")
    assert "Generic1" not in home_pg.data.decode("UTF-8")
    
@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_previous_button_available_on_second_pg(client):
    home_pg = client.get("/?pg=2")
    assert "&laquo; Previous" in home_pg.data.decode("UTF-8")
    
@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_previous_button_notavailable_on_first_pg(client):
    home_pg = client.get("/")
    assert "&laquo; Previous" not in home_pg.data.decode("UTF-8")
    
@log_user(2, "John Doe", "John@mail", "regular")
@configure(True)
def test_previous_and_next_available_middle_pg(client):
    to_delete_ids = []
    i = 0
    while i < 6:
        to_delete_ids.append(add_disposable_post())
        i += 1
    home_pg = client.get("/?pg=2")
    assert "&laquo; Previous", home_pg.data.decode("UTF-8")
    assert "Next", home_pg.data.decode("UTF-8")
    id : int
    for id in to_delete_ids:
        Posts().remove(id)