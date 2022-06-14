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
def test_post_not_rendered_on_server(client):
    pass

@configure(True)
def test_route_returns_json(client):
    pass
