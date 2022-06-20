from urllib.error import HTTPError
from flask import Blueprint, jsonify, abort
from models.posts_schema import PostsJsonSchema
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo

class PostApi:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.posts = repo
        self.bp = Blueprint("api_route", __name__)
        self.route = self.register("/post/<post_id>/", self.api_route)
        self.posts_schema = PostsJsonSchema()
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get"])(func)

    def api_route(self, post_id):
        post = self.posts.get(post_id)
        if not post:
            abort(404)
        else:
            res = self.posts_schema.dump(post)
            data = jsonify(res)
            return data
