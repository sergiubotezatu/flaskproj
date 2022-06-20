from flask import Flask
from pytest import fixture, FixtureRequest
from werkzeug import Request
from tests.helpers import configure

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
    assert result.status_code == 404

@configure(True)
def test_html_not_rendered_on_server_side(client):
    result = client.get("/post/api/1/")
    assert "var id = JSON.parse('1')" in result.data.decode("UTF-8")
    assert "window.onload = get_post(id)" in result.data.decode("UTF-8")