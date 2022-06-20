from flask import Flask
from pytest import fixture

from tests.helpers import configure

BASE_POST = "/post/"

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@configure(True)
def test_front_pg_displays_all_filterable_users(client):
    result = client.get("/")
    assert '<a href="/?user_id=1&amp;name=Mark Doe&amp;">Mark Doe</a>' in result.data.decode("UTF-8")
    assert '<a href="/?user_id=2&amp;name=John Doe&amp;">John Doe</a>' in result.data.decode("UTF-8")
    
@configure(True)
def test_front_pg_displays_only_filtered_users_post(client):
    unfiltered_home = client.get("/")
    assert 2 ==  unfiltered_home.data.decode("UTF-8").count("by Mark Doe")
    filtered = client.get("/?user_id=2&name=John&")
    assert 0 == filtered.data.decode("UTF-8").count("by Mark Doe")
    assert 3 == filtered.data.decode("UTF-8").count("by John Doe")

@configure(True)
def test_front_pg_displays_multiple_filtered_users(client):
    filtered = client.get("/?user_id=1&name=Mark Doe&user_id=2&name=John Doe&pg=1")
    assert 2 == filtered.data.decode("UTF-8").count("by Mark Doe")
    assert 3 == filtered.data.decode("UTF-8").count("by John Doe")

@configure(True)
def test_page_change_doesnot_affect_filters(client):
    filtered = client.get("/?user_id=1&name=Mark Doe&user_id=2&name=John Doe&pg=2")
    assert 0 == filtered.data.decode("UTF-8").count("by John Doe")
    assert 1 == filtered.data.decode("UTF-8").count("by Mark Doe")