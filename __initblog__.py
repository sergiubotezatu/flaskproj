from flask import Flask
from view.home import home
from view.post_view import post

def create_blog(is_test_app = False):
    blog = Flask(__name__)
    blog.secret_key = "FlaskBlog"
    blog.config["TESTING"] = is_test_app
    blog.register_blueprint(home, url_prefix="/")
    blog.register_blueprint(post, url_prefix="/post")

    return blog
