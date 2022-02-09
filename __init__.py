from flask import Flask, Blueprint
from view.home import home
from view.post_view import post

def create_blog():
    blog = Flask(__name__)
    blog.config["Secret_key"]= "FlaskBlog"
    blog.register_blueprint(home, url_prefix="/")
    blog.register_blueprint(post, url_prefix="/post")

    return blog
