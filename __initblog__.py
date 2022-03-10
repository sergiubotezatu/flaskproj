from flask import Flask
from services.idata_base import IDataBase
from services.services import Services
from models.container import Container
from services.ipost_repo import IPostRepo


def create_blog(is_test_app = False):
    blog = Flask(__name__)
    blog.config["TESTING"] = is_test_app
    blog.secret_key = "FlaskTest" if is_test_app else "FlaskBlog"
    Services.container = Container().get(is_test_app)

    from view.home import Home
    blog.register_blueprint(Home(IPostRepo).bp, url_prefix="/")
    from view.post_view import PostPage
    blog.register_blueprint(PostPage(IPostRepo).bp, url_prefix="/post")
    from view.db_setup import DbSetUp
    blog.register_blueprint(DbSetUp(IDataBase).bp)

    return blog
