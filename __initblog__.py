from flask import Flask
from services.posts_factory import PostsFactory
from services.seed import blogPosts

def create_blog(is_test_app = False):
    blog = Flask(__name__)
    blog.config["TESTING"] = is_test_app
    blog.secret_key = "FlaskTest" if is_test_app else "FlaskBlog"
    repo = PostsFactory.create(is_test_app)
        
    from view.home import Home
    blog.register_blueprint(Home(repo).bp, url_prefix="/")
    from view.post_view import PostPage
    blog.register_blueprint(PostPage(repo).bp, url_prefix="/post")
    from view.db_setup import DbSetUp
    blog.register_blueprint(DbSetUp(repo).bp, url_prefix = "/")

    return blog
