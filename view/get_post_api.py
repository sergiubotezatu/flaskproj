from flask import request
from flask import Blueprint, jsonify, render_template
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
        self.loaded = False
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get"])(func)

    def api_route(self, post_id):
        if not self.loaded:
            self.loaded = True
            return render_template("api_read.html", id = post_id)
        post = self.posts.get(post_id)
        res = self.posts_schema.dump(post)
        data = jsonify(res)
        self.loaded = False
        return data
