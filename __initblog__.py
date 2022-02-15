from flask import Flask
from view.home import home
from view.post_view import post
from services import seed
from services import posts_factory

def create_blog(is_test_app = False):
    blog = Flask(__name__)
    blog.config["TESTING"] = is_test_app
    blog.secret_key = "FlaskTest" if is_test_app else "FlaskBlog"
    seed.source_factory = posts_factory.Create(blog.secret_key)
    blog.register_blueprint(home, url_prefix="/")
    blog.register_blueprint(post, url_prefix="/post")

    return blog
