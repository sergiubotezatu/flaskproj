import json
from flask import Flask, request
from pytest import fixture
import __init__
from services.interfaces.ipost_repo import IPostRepo
from tests.helpers import configure
from view.get_post_api import PostApi

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@configure(True)
def test_succesful_request(client):
    result = client.get("/api/post/1/")
    assert result.status_code == 200

@configure(True)
def test_api_route_returns_json(client):
    result = client.get("/api/post/1/")
    assert result.headers[0] == ('Content-Type', 'application/json')
    
@configure(True)
def test_api_route_returns_correct_post(client):
    result = client.get("/api/post/1/")
    json = result.json
    assert "Mark Doe" == json["auth"]
    assert "Test post 1" == json["content"]
    assert "Generic1" == json["title"]

@configure(True)
def test_404_if_post_not_found(client):
    result = client.get("/api/post/12/")
    json = result.json
    assert "404. NOT FOUND" == json["error"]

@configure(True)
def test_html_not_rendered_on_server_side(client):
    result = client.get("/post/api/1/")
    assert "Mark Doe" not in result.data.decode("UTF-8")
